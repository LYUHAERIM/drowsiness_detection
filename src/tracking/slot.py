"""
슬롯 기반 다중 인물 트래킹.

Zoom 썸네일 레이아웃에서 YOLO 탐지 결과를 슬롯에 매칭하고
슬롯별 상태(이름, 졸음 타이머, bbox 등)를 유지합니다.
"""
import math
from collections import deque
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from scipy.optimize import linear_sum_assignment


@dataclass
class SlotState:
    """
    한 명의 수강생을 추적하는 슬롯 상태.

    탐지 정보 + OCR 이름 + 졸음 감지 타이머를 하나의 dataclass로 관리.
    TemporalAnalyzer처럼 한 슬롯 == 한 수강생으로 동작.
    """
    slot_id: int
    box: tuple                     # (x1, y1, x2, y2) 픽셀 좌표
    class_name: str                # "person_on" | "person_off" | "screen_off"
    conf: float
    last_seen_frame: int
    misses: int = 0                # 연속으로 탐지 못한 프레임 수

    # ── OCR / 이름 ───────────────────────────────────────────────────────────
    name_votes: list = field(default_factory=list)
    name_final: str = ""
    name_conf: float = 0.0
    last_ocr_frame: int = -10000
    is_teacher: bool = False

    # ── EMA 기준선 ────────────────────────────────────────────────────────────
    bl_ear: Optional[float] = None
    bl_mar: Optional[float] = None
    bl_pitch: Optional[float] = None
    bl_center_y: Optional[float] = None

    # ── 졸음 타이머 (Level1) ──────────────────────────────────────────────────
    ear_low_frames: int = 0
    pitch_high_frames: int = 0
    tilt_high_frames: int = 0
    mar_high_frames: int = 0

    # ── Level2 타이머 ─────────────────────────────────────────────────────────
    face_low_frames: int = 0

    # ── 회복 / hold ───────────────────────────────────────────────────────────
    recover_frames: int = 0
    drowsy_hold_frames: int = 0

    # ── 이탈 카운터 ───────────────────────────────────────────────────────────
    absent_hold: int = 0
    present_hold: int = 0

    # ── PERCLOS 히스토리 ──────────────────────────────────────────────────────
    eye_closed_hist: deque = field(default_factory=lambda: deque(maxlen=300))

    # ── 스무딩 히스토리 ───────────────────────────────────────────────────────
    raw_hist: deque = field(default_factory=lambda: deque(maxlen=20))
    current_state: str = "NORMAL"

    # ── NoFace 연속 카운터 ────────────────────────────────────────────────────
    noface_consec: int = 0          # 연속 얼굴 미검출 프레임 수
    last_drowsy_ts: float = -1.0    # 마지막 DROWSY 감지 타임스탬프 (초)

    # ── Wakeup 감지 ───────────────────────────────────────────────────────────
    wake_motion_frames: int = 0     # 연속 큰 움직임 프레임 수 (wakeup 감지용)

    # ── bbox 안정화 ───────────────────────────────────────────────────────────
    box_smoothed: Optional[list] = None
    prev_gray: Optional[np.ndarray] = None

    # ── 통계 ──────────────────────────────────────────────────────────────────
    total_frames: int = 0
    frames_drowsy: int = 0
    frames_yawn: int = 0
    frames_absent: int = 0
    frames_normal: int = 0


# ─────────────────────────────────────────────────────────────────────────────
# 내부 헬퍼
# ─────────────────────────────────────────────────────────────────────────────

def _center_of(box: tuple) -> np.ndarray:
    x1, y1, x2, y2 = box
    return np.array([(x1 + x2) / 2.0, (y1 + y2) / 2.0], dtype=np.float32)


def _iou_xyxy(a: tuple, b: tuple) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1 = max(ax1, bx1); iy1 = max(ay1, by1)
    ix2 = min(ax2, bx2); iy2 = min(ay2, by2)
    inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
    union = (ax2 - ax1) * (ay2 - ay1) + (bx2 - bx1) * (by2 - by1) - inter + 1e-6
    return inter / union


# ─────────────────────────────────────────────────────────────────────────────
# 퍼블릭 유틸
# ─────────────────────────────────────────────────────────────────────────────

def sort_detections_reading_order(dets: list[dict], row_thresh: int = 90) -> list[dict]:
    """
    탐지 결과를 읽기 순서(위→아래, 좌→우)로 정렬.

    Args:
        dets: [{"box": (x1,y1,x2,y2), "cls": str, "conf": float}, ...]
        row_thresh: 같은 행으로 묶는 y 거리 임계값 (px)
    """
    if not dets:
        return []

    rows: list[dict] = []
    for det in sorted(dets, key=lambda d: (_center_of(d["box"])[1], _center_of(d["box"])[0])):
        cy = _center_of(det["box"])[1]
        placed = False
        for row in rows:
            if abs(row["mean_y"] - cy) <= row_thresh:
                row["items"].append(det)
                row["mean_y"] = float(np.mean([_center_of(x["box"])[1] for x in row["items"]]))
                placed = True
                break
        if not placed:
            rows.append({"mean_y": float(cy), "items": [det]})

    out: list[dict] = []
    for row in sorted(rows, key=lambda r: r["mean_y"]):
        out.extend(sorted(row["items"], key=lambda d: _center_of(d["box"])[0]))
    return out


def detect_layout_change(prev_summary: Optional[dict], curr_summary: dict) -> bool:
    """
    클래스별 탐지 수가 1개 이상 변하면 레이아웃 변경으로 판단.

    Args:
        prev_summary: 이전 프레임 {cls: count}
        curr_summary: 현재 프레임 {cls: count}
    """
    if prev_summary is None:
        return False
    for key in ("screen_off", "person_on", "person_off"):
        if abs(curr_summary.get(key, 0) - prev_summary.get(key, 0)) >= 1:
            return True
    return False


def stabilize_bbox(prev: Optional[list], new: tuple, alpha: float = 0.25, max_shift: int = 20) -> list:
    """
    EMA + 최대 이동량 제한으로 바운딩박스를 안정화.

    Args:
        prev: 이전 smoothed bbox [x1,y1,x2,y2] or None
        new: 새 bbox (x1,y1,x2,y2)
        alpha: EMA 가중치 (클수록 빠르게 반응)
        max_shift: 한 프레임에 이동할 수 있는 최대 픽셀
    """
    if prev is None:
        return list(new)

    px1, py1, px2, py2 = prev
    nx1, ny1, nx2, ny2 = new

    pcx = (px1 + px2) / 2; pcy = (py1 + py2) / 2
    ncx = (nx1 + nx2) / 2; ncy = (ny1 + ny2) / 2

    dcx = float(np.clip(ncx - pcx, -max_shift, max_shift))
    dcy = float(np.clip(ncy - pcy, -max_shift, max_shift))
    lcx = pcx + dcx; lcy = pcy + dcy

    pw = px2 - px1; ph = py2 - py1
    nw = nx2 - nx1; nh = ny2 - ny1
    lw = pw + float(np.clip(nw - pw, -pw * 0.15, pw * 0.15))
    lh = ph + float(np.clip(nh - ph, -ph * 0.15, ph * 0.15))

    lb = [lcx - lw / 2, lcy - lh / 2, lcx + lw / 2, lcy + lh / 2]
    return [prev[i] * (1 - alpha) + lb[i] * alpha for i in range(4)]


def match_slots_to_detections(
    slots: dict[int, SlotState],
    dets: list[dict],
    frame_w: int,
    frame_h: int,
    match_dist: float = 0.40,
) -> tuple[list[tuple[int, int]], list[int], list[int]]:
    """
    Hungarian algorithm으로 기존 슬롯과 새 탐지 결과를 매칭.

    비용 = 정규화 거리 - 0.2 * IoU (대각선 기준 정규화)

    Args:
        slots: {slot_id: SlotState}
        dets:  [{"box": ..., "cls": ..., "conf": ...}, ...]
        frame_w, frame_h: 프레임 크기
        match_dist: 매칭 허용 최대 정규화 거리

    Returns:
        matches:         [(slot_id, det_idx), ...]
        unmatched_slots: [slot_id, ...]
        unmatched_dets:  [det_idx, ...]
    """
    if not slots or not dets:
        return [], list(slots.keys()), list(range(len(dets)))

    sids = list(slots.keys())
    diag = math.sqrt(frame_w ** 2 + frame_h ** 2)
    cost = np.full((len(sids), len(dets)), 1e6, dtype=np.float32)

    for i, sid in enumerate(sids):
        sc = _center_of(slots[sid].box)
        for j, det in enumerate(dets):
            dc = _center_of(det["box"])
            dist = float(np.linalg.norm(sc - dc)) / max(diag, 1.0)
            iou = _iou_xyxy(slots[sid].box, det["box"])
            cost[i, j] = dist - 0.2 * iou

    row_ind, col_ind = linear_sum_assignment(cost)

    matches: list[tuple[int, int]] = []
    um_slots: set[int] = set(sids)
    um_dets: set[int] = set(range(len(dets)))

    for r, c in zip(row_ind, col_ind):
        sid = sids[r]
        dist = float(np.linalg.norm(
            _center_of(slots[sid].box) - _center_of(dets[c]["box"])
        )) / max(diag, 1.0)
        if dist <= match_dist:
            matches.append((sid, c))
            um_slots.discard(sid)
            um_dets.discard(c)

    return matches, list(um_slots), list(um_dets)
