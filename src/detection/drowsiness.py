"""
v6 계층 룰베이스 졸음 감지 상태 머신.

Level1 (FaceMesh 검출 성공):
    EAR (메인) + MAR / pitch_like / tilt_deg / PERCLOS (보조) 조합

Level2 (FaceDetection fallback):
    face_center_y 하강 (단독으로는 DROWSY 진입 불가 → hold 전용)

Level3 (motion):
    낮은 움직임 감지 시 DROWSY 상태를 최대 N초 추가 유지

EMA 기준선: NORMAL 상태 프레임에서만 갱신하여 개인차 적응.

졸음 감지 로직을 수정하려면 이 파일만 수정하면 됩니다.
"""
import math
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

import cv2
import numpy as np


@dataclass
class DrowsinessConfig:
    """
    졸음 감지 파라미터.

    인스턴스를 만들어 PipelineConfig.drowsiness 에 전달하거나
    update_drowsiness_state() 에 직접 넘겨 임계값을 조정할 수 있습니다.
    """
    # EMA 기준선 수렴 속도
    ema_alpha_fast: float = 0.05    # 초기 30초: 빠른 수렴
    ema_alpha_slow: float = 0.01    # 이후: 안정적 유지
    ema_fast_sec: float = 30.0

    # Level1: EAR
    ear_ratio: float = 0.75         # baseline 대비 이 비율 미만 = 눈 감김
    ear_init_abs: float = 0.18      # baseline 수렴 전 절대 임계값
    ear_hold_strong_sec: float = 0.5   # EAR + 보조 신호 → DROWSY 진입 시간
    ear_hold_weak_sec: float = 1.5     # EAR 단독 → DROWSY 진입 시간

    # Level1: PERCLOS
    perclos_window_sec: float = 20.0
    perclos_thresh: float = 0.20

    # Level1: MAR
    mar_init_abs: float = 0.60
    mar_ratio: float = 1.30
    mar_hold_sec: float = 0.5

    # Level1: Pitch
    pitch_delta_thresh: float = 0.10   # baseline 대비 증가량
    pitch_hold_sec: float = 1.0

    # Level1: Tilt
    tilt_deg_thresh: float = 15.0
    tilt_hold_sec: float = 1.0

    # Level2: 얼굴 위치 fallback
    face_y_delta_thresh: float = 0.08
    face_y_hold_sec: float = 2.0

    # Level3: motion hold
    low_motion_th: float = 5.0
    drowsy_hold_ext_sec: float = 3.0

    # 회복 / 스무딩
    recover_sec: float = 0.3
    absent_hold_sec: float = 0.8
    absent_recover_sec: float = 0.5
    smooth_window_sec: float = 0.5


# ─────────────────────────────────────────────────────────────────────────────
# 모션 계산 (Level3 입력)
# ─────────────────────────────────────────────────────────────────────────────

def compute_motion(
    prev_gray: Optional[np.ndarray],
    curr_gray: Optional[np.ndarray],
    face_box: Optional[tuple] = None,
    thumb_shape: Optional[tuple] = None,
) -> float:
    """
    두 그레이스케일 프레임 간 픽셀 차이로 움직임 강도를 계산.

    face_box가 있으면 얼굴 영역만, 없으면 썸네일 상단 70% 영역 사용.

    Returns:
        움직임 강도 (float). 검출 불가 시 nan.
    """
    _nan = float("nan")
    if prev_gray is None or curr_gray is None:
        return _nan
    if prev_gray.shape != curr_gray.shape:
        return _nan

    diff = cv2.absdiff(prev_gray, curr_gray)

    if face_box:
        x1, y1, x2, y2 = face_box
        x1 = max(0, x1); y1 = max(0, y1)
        x2 = min(diff.shape[1], x2); y2 = min(diff.shape[0], y2)
        if x2 > x1 and y2 > y1:
            diff = diff[y1:y2, x1:x2]
    elif thumb_shape:
        h = thumb_shape[0]
        diff = diff[:int(h * 0.7), :]

    return float(np.mean(diff)) if diff.size > 0 else _nan


# ─────────────────────────────────────────────────────────────────────────────
# 내부 헬퍼
# ─────────────────────────────────────────────────────────────────────────────

def _isnan(v) -> bool:
    return v is None or (isinstance(v, float) and math.isnan(v))


def _ema_update(old: Optional[float], new: float, alpha: float) -> Optional[float]:
    if _isnan(new):
        return old
    if old is None or _isnan(old):
        return float(new)
    return float(old * (1 - alpha) + new * alpha)


def _get_ema_alpha(ts: float, cfg: DrowsinessConfig) -> float:
    return cfg.ema_alpha_fast if ts < cfg.ema_fast_sec else cfg.ema_alpha_slow


def _reset_timers(slot) -> None:
    slot.ear_low_frames = 0
    slot.pitch_high_frames = 0
    slot.tilt_high_frames = 0
    slot.mar_high_frames = 0
    slot.face_low_frames = 0
    slot.recover_frames = 0
    slot.drowsy_hold_frames = 0


# ─────────────────────────────────────────────────────────────────────────────
# 퍼블릭 함수
# ─────────────────────────────────────────────────────────────────────────────

def update_baselines(slot, face_result, final_state: str, ts: float, cfg: DrowsinessConfig) -> None:
    """
    NORMAL 상태일 때만 슬롯의 EMA 기준선(baseline)을 갱신.

    강사 슬롯은 기준선 갱신 제외.
    """
    if final_state != "NORMAL" or slot.is_teacher:
        return
    alpha = _get_ema_alpha(ts, cfg)
    slot.bl_ear      = _ema_update(slot.bl_ear,      face_result.ear,           alpha)
    slot.bl_mar      = _ema_update(slot.bl_mar,      face_result.mar,           alpha)
    slot.bl_pitch    = _ema_update(slot.bl_pitch,    face_result.pitch_like,    alpha)
    slot.bl_center_y = _ema_update(slot.bl_center_y, face_result.face_center_y, alpha)


def update_drowsiness_state(
    slot,
    face_result,
    motion: float,
    cls_name: str,
    fps: float,
    ts: float,
    cfg: Optional[DrowsinessConfig] = None,
) -> tuple[str, str, str]:
    """
    슬롯의 졸음 상태를 한 프레임 업데이트.

    슬롯 내부 타이머·카운터를 in-place 수정하고 상태를 반환합니다.

    Args:
        slot:        SlotState (tracking/slot.py)
        face_result: FaceMeshResult (detection/face.py)
        motion:      compute_motion() 결과
        cls_name:    YOLO 클래스명
        fps:         영상 FPS
        ts:          현재 타임스탬프 (초)
        cfg:         DrowsinessConfig (None이면 기본값 사용)

    Returns:
        (raw_state, final_state, drowsy_reason)
        - raw_state:    스무딩 전 이번 프레임 판단 ("NORMAL" | "DROWSY" | "ABSENT" | "IGNORE")
        - final_state:  스무딩·회복 타이머 적용 후 최종 상태
        - drowsy_reason: DROWSY 진입 이유 문자열 (디버깅용)
    """
    if cfg is None:
        cfg = DrowsinessConfig()

    # ── ABSENT ───────────────────────────────────────────────────────────────
    if cls_name in {"person_off", "screen_off"}:
        slot.absent_hold += 1
        slot.present_hold = 0
        _reset_timers(slot)
        slot.raw_hist.append("ABSENT")
        if slot.absent_hold >= int(cfg.absent_hold_sec * fps):
            slot.current_state = "ABSENT"
        return "ABSENT", slot.current_state, "absent"

    slot.present_hold += 1
    slot.absent_hold = max(0, slot.absent_hold - 1)
    if slot.absent_hold == 0 and slot.present_hold >= int(cfg.absent_recover_sec * fps):
        if slot.current_state == "ABSENT":
            slot.current_state = "NORMAL"

    # ── IGNORE (강사) ─────────────────────────────────────────────────────────
    if slot.is_teacher:
        slot.current_state = "IGNORE"
        return "IGNORE", "IGNORE", "teacher"

    ear      = face_result.ear
    pitch    = face_result.pitch_like
    tilt     = face_result.tilt_deg
    center_y = face_result.face_center_y
    lm_ok    = face_result.lm_ok

    ear_th = slot.bl_ear * cfg.ear_ratio if slot.bl_ear else cfg.ear_init_abs

    # PERCLOS 갱신
    if not _isnan(ear):
        slot.eye_closed_hist.append(1 if ear < ear_th else 0)
    perclos = float("nan")
    min_hist = int(cfg.perclos_window_sec * fps * 0.3)
    if len(slot.eye_closed_hist) >= min_hist:
        perclos = float(np.mean(list(slot.eye_closed_hist)))

    # 보조 신호 플래그
    pitch_high = False
    if not _isnan(pitch):
        pitch_high = (pitch > slot.bl_pitch + cfg.pitch_delta_thresh) if slot.bl_pitch else (pitch > 0.20)
    tilt_high  = not _isnan(tilt) and tilt > cfg.tilt_deg_thresh
    perclos_hi = not _isnan(perclos) and perclos >= cfg.perclos_thresh

    # face_low_frames: lm_ok 무관하게 항상 갱신
    if not _isnan(center_y):
        _face_low = (
            center_y > slot.bl_center_y + cfg.face_y_delta_thresh
            if slot.bl_center_y else center_y > 0.60
        )
        slot.face_low_frames = slot.face_low_frames + 1 if _face_low else max(0, slot.face_low_frames - 1)
    else:
        slot.face_low_frames = max(0, slot.face_low_frames - 1)

    # Level1 타이머 갱신
    if lm_ok:
        slot.ear_low_frames    = slot.ear_low_frames + 1    if not _isnan(ear) and ear < ear_th else max(0, slot.ear_low_frames - 2)
        slot.pitch_high_frames = slot.pitch_high_frames + 1 if pitch_high else max(0, slot.pitch_high_frames - 2)
        slot.tilt_high_frames  = slot.tilt_high_frames + 1  if tilt_high  else max(0, slot.tilt_high_frames - 2)
        _mar    = face_result.mar
        _mar_th = slot.bl_mar * cfg.mar_ratio if slot.bl_mar else cfg.mar_init_abs
        _mar_high = not _isnan(_mar) and _mar > _mar_th
        slot.mar_high_frames = slot.mar_high_frames + 1 if _mar_high else max(0, slot.mar_high_frames - 2)
    else:
        slot.ear_low_frames    = max(0, slot.ear_low_frames - 1)
        slot.pitch_high_frames = max(0, slot.pitch_high_frames - 1)
        slot.tilt_high_frames  = max(0, slot.tilt_high_frames - 1)
        slot.mar_high_frames   = max(0, slot.mar_high_frames - 1)

    # 졸음 판별 (Level1)
    ear_strong = slot.ear_low_frames    >= int(cfg.ear_hold_strong_sec * fps)
    ear_weak   = slot.ear_low_frames    >= int(cfg.ear_hold_weak_sec   * fps)
    pitch_flag = slot.pitch_high_frames >= int(cfg.pitch_hold_sec * fps)
    tilt_flag  = slot.tilt_high_frames  >= int(cfg.tilt_hold_sec  * fps)
    mar_flag   = slot.mar_high_frames   >= int(cfg.mar_hold_sec   * fps)
    face_flag  = slot.face_low_frames   >= int(cfg.face_y_hold_sec * fps)

    drowsy_reason = ""
    if lm_ok:
        aux = sum([pitch_flag, tilt_flag, perclos_hi, mar_flag])
        if   ear_strong and aux >= 1:       drowsy_reason = f"EAR+aux({aux})"
        elif ear_weak:                      drowsy_reason = "EAR_alone"
        elif perclos_hi and pitch_flag:     drowsy_reason = "PERCLOS+pitch"
        elif tilt_flag  and pitch_flag:     drowsy_reason = "tilt+pitch"
        elif mar_flag   and pitch_flag:     drowsy_reason = "MAR+pitch"
        elif mar_flag   and ear_strong:     drowsy_reason = "MAR+EAR"

    # Level2: face_center_y fallback
    if not drowsy_reason and face_flag:
        drowsy_reason = "L2_face_low"

    # Level3: motion hold
    low_motion = not _isnan(motion) and motion < cfg.low_motion_th
    if slot.current_state == "DROWSY" and not drowsy_reason:
        if low_motion:
            slot.drowsy_hold_frames += 1
            if slot.drowsy_hold_frames <= int(cfg.drowsy_hold_ext_sec * fps):
                drowsy_reason = f"L3_hold({slot.drowsy_hold_frames}f)"
        else:
            slot.drowsy_hold_frames = 0

    if drowsy_reason:
        if lm_ok:
            slot.drowsy_hold_frames = 0
        raw = "DROWSY"
    else:
        slot.drowsy_hold_frames = 0
        raw = "NORMAL"

    # 회복 타이머
    if slot.current_state == "DROWSY" and raw == "NORMAL":
        ear_ok   = lm_ok and not _isnan(ear) and ear >= ear_th
        pitch_ok = not pitch_high
        slot.recover_frames = slot.recover_frames + 1 if (ear_ok and pitch_ok) else 0
    else:
        slot.recover_frames = 0

    # 스무딩 → 최종 상태 전환
    smooth_n = max(1, int(cfg.smooth_window_sec * fps))
    slot.raw_hist.append(raw)
    smoothed = Counter(list(slot.raw_hist)[-smooth_n:]).most_common(1)[0][0]

    prev = slot.current_state
    if prev not in {"ABSENT", "IGNORE"}:
        if smoothed == "DROWSY":
            slot.current_state = "DROWSY"
        elif smoothed == "NORMAL":
            if prev == "DROWSY":
                if slot.recover_frames >= int(cfg.recover_sec * fps):
                    slot.current_state = "NORMAL"
            else:
                slot.current_state = "NORMAL"

    return raw, slot.current_state, drowsy_reason
