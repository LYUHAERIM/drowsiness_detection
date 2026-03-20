"""
Zoom 썸네일 영상 졸음 감지 파이프라인.

실행:
    uv run python scripts/infer_video.py

파이프라인 흐름:
    VideoReader → YOLO → SlotTracking → OCR → FaceMeshDetector
        → DrowsinessState → Annotate → VideoWriter + CSV

각 기능 로직 수정:
    YOLO 탐지         → src/models/yolo_trainer.py
    슬롯 트래킹       → src/tracking/slot.py
    OCR 이름 추출     → src/ocr/reader.py
    얼굴 특징 추출    → src/detection/face.py  (FaceMeshDetector)
    졸음 판별 로직    → src/detection/drowsiness.py
    화면 시각화       → src/visual/annotator.py
    영상 입출력       → src/utils/video_conversion.py
"""
import argparse
import csv
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

import cv2
import numpy as np
import torch
from ultralytics import YOLO
from tqdm import tqdm

from src.detection.drowsiness import (
    DrowsinessConfig,
    _reset_timers,
    compute_motion,
    update_baselines,
    update_drowsiness_state,
)
from src.detection.face import FaceMeshDetector
from src.detection.pose import PoseDetector
from src.ocr.reader import NameOCR
from src.tracking.slot import (
    SlotState,
    detect_layout_change,
    match_slots_to_detections,
    sort_detections_reading_order,
    stabilize_bbox,
)
from src.utils.loaders import load_env
from src.utils.video_conversion import VideoReader, VideoWriter
from src.visual.annotator import (
    INFO_BOX_H,
    draw_face_box,
    draw_info_box,
    draw_slot_bbox,
)

# ─────────────────────────────────────────────────────────────────────────────
# 시각화 색상 상수
# ─────────────────────────────────────────────────────────────────────────────

BOX_COLORS = {
    "person_on":  (60, 220, 60),
    "person_off": (0, 180, 255),
    "screen_off": (0, 100, 255),
    "unknown":    (180, 180, 180),
}
STATE_COLORS = {
    "NORMAL": (70, 220, 70),
    "DROWSY": (0, 0, 255),      # 빨간색 (BGR)
    "YAWN":   (0, 128, 255),    # 주황색 (BGR)
    "ABSENT": (0, 165, 255),
    "IGNORE": (160, 160, 160),
}


# ─────────────────────────────────────────────────────────────────────────────
# PipelineConfig
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class PipelineConfig:
    """
    ZoomPipeline 전체 설정.

    각 서브모듈 파라미터를 한 곳에서 관리합니다.
    세부 졸음 임계값은 drowsiness 필드(DrowsinessConfig)에서 조정하세요.
    """
    # 영상 범위
    start_sec: float = 0.0
    end_sec: Optional[float] = None
    target_fps: float = 10.0

    # YOLO
    yolo_imgsz: int = 960 # 640 Test > 960 > 1280
    yolo_conf: float = 0.10
    yolo_iou: float = 0.45
    yolo_max_det: int = 5 # 20 -> 5 수정

    # 슬롯 트래킹
    slot_max_misses: int = 40       # 슬롯 삭제까지 허용 miss 프레임 수
    slot_match_dist: float = 0.40   # 슬롯-탐지 매칭 최대 정규화 거리
    row_group_thresh: int = 90      # 같은 행으로 묶는 y 거리 (px)

    # OCR
    ocr_retry_interval: int = 90    # 일반 OCR 재시도 간격 (프레임)
    ocr_fast_interval: int = 20     # 레이아웃 변경 직후 빠른 OCR 간격
    name_vote_maxlen: int = 12      # 이름 투표 기록 최대 길이
    ocr_lock_min_votes: int = 3     # 이름 확정 최소 득표 수
    ocr_name_conf_lock: float = 0.70  # 이 신뢰도 이상이면 OCR 재시도 안 함
    layout_boost_sec: float = 3.0   # 레이아웃 변경 후 빠른 OCR 지속 시간
    layout_change_cooldown: float = 2.0  # 레이아웃 변경 감지 최소 간격 (초)
    teacher_names: list = field(default_factory=list)  # 강사 이름 목록

    # FaceMesh
    face_min_conf: float = 0.25
    use_clahe: bool = True

    # No Face: 연속 N프레임 이상 미검출 시 NOFACE 확정 (순간 가림 필터링)
    noface_hold_frames: int = 15    # ≈1.5초 @ 10fps

    # Pose fallback (FaceMesh lm_ok=False일 때 PoseDetector로 고개 숙임 감지)
    use_pose_fallback: bool = False
    pose_conf: float = 0.5          # PoseDetector 검출 최소 신뢰도
    pose_consec_frames: int = 90    # 연속 감지 프레임 수 (≈3초 @ 30fps)

    # 졸음 감지 (세부 임계값)
    drowsiness: DrowsinessConfig = field(default_factory=DrowsinessConfig)

    # 시각화
    info_box_w: int = 340

    # 디바이스
    device: int | str = field(
        default_factory=lambda: 0 if torch.cuda.is_available() else "cpu"
    )


# ─────────────────────────────────────────────────────────────────────────────
# ZoomPipeline
# ─────────────────────────────────────────────────────────────────────────────

class ZoomPipeline:
    """
    Zoom 썸네일 영상 졸음/이탈 감지 파이프라인.

    YOLO → Slot Tracking → OCR → FaceMesh → DrowsinessState → Annotate

    사용 예시::

        config = PipelineConfig(teacher_names=["강경미"], target_fps=10)
        pipeline = ZoomPipeline(yolo_model, config)

        with VideoReader(video_path, target_fps=config.target_fps) as reader:
            with VideoWriter(out_path, reader.fps_effective,
                             reader.width + config.info_box_w, reader.height) as writer:
                with pipeline:
                    for frame_idx, ts, frame in reader:
                        canvas, records = pipeline.process_frame(frame, frame_idx, reader.fps)
                        writer.write(canvas)
    """

    def __init__(self, yolo_model, config: Optional[PipelineConfig] = None):
        self._model = yolo_model
        self._cfg = config or PipelineConfig()
        self._face_detector: Optional[FaceMeshDetector] = None
        self._pose_detector: Optional[PoseDetector] = None
        self._ocr: Optional[NameOCR] = None

        self._slots: dict[int, SlotState] = {}
        self._next_slot_id = 1
        self._prev_layout_summary: Optional[dict] = None
        self._last_layout_change_frame = -(10 ** 9)
        self._layout_boost_until = -1
        self._pose_consec: dict[int, int] = {}  # slot_id → 연속 pose_head_down 프레임 수

    # ── 컨텍스트 매니저 ───────────────────────────────────────────────────────

    def open(self) -> "ZoomPipeline":
        cfg = self._cfg
        self._face_detector = FaceMeshDetector(
            min_detection_confidence=cfg.face_min_conf,
            use_clahe=cfg.use_clahe,
        )
        if cfg.use_pose_fallback:
            self._pose_detector = PoseDetector(
                min_detection_confidence=cfg.pose_conf,
            )
        self._ocr = NameOCR(
            teacher_names=cfg.teacher_names,
            gpu=isinstance(cfg.device, int),
        )
        return self

    def close(self):
        if self._face_detector:
            self._face_detector.close()
        if self._pose_detector:
            self._pose_detector.close()

    def __enter__(self) -> "ZoomPipeline":
        return self.open()

    def __exit__(self, *_):
        self.close()

    # ── 메인 처리 ─────────────────────────────────────────────────────────────

    def process_frame(
        self,
        frame: np.ndarray,
        frame_idx: int,
        fps: float,
        fps_effective: Optional[float] = None,
    ) -> tuple[np.ndarray, list[dict]]:
        """
        프레임 한 장을 처리합니다.

        Args:
            frame:         BGR 이미지
            frame_idx:     원본 영상 기준 프레임 번호
            fps:           원본 영상 FPS (타임스탬프 계산용)
            fps_effective: 실제 처리 FPS (threshold 계산용; None이면 fps와 동일)

        Returns:
            canvas:  어노테이션된 BGR 이미지 (frame_w + info_box_w 너비)
            records: 슬롯별 결과 dict 리스트 (CSV 저장용)
        """
        cfg = self._cfg
        ts = frame_idx / max(fps, 1e-6)
        fps_eff = fps_effective if fps_effective is not None else fps  # threshold 계산용
        frame_h, frame_w = frame.shape[:2]

        # ── YOLO 탐지 ─────────────────────────────────────────────────────────
        dets = self._yolo_detect(frame)
        dets = sort_detections_reading_order(dets, cfg.row_group_thresh)

        # ── 레이아웃 변화 감지 ─────────────────────────────────────────────────
        curr_layout = dict(Counter(d["cls"] for d in dets))
        if detect_layout_change(self._prev_layout_summary, curr_layout):
            cooldown = int(cfg.layout_change_cooldown * fps)
            if frame_idx - self._last_layout_change_frame >= cooldown:
                self._last_layout_change_frame = frame_idx
                self._layout_boost_until = frame_idx + int(cfg.layout_boost_sec * fps)
                for s in self._slots.values():
                    s.name_votes = s.name_votes[-1:]
                    s.name_final = ""
        self._prev_layout_summary = curr_layout

        # ── 슬롯 매칭 ─────────────────────────────────────────────────────────
        matches, um_slots, um_dets = match_slots_to_detections(
            self._slots, dets, frame_w, frame_h, cfg.slot_match_dist
        )
        for sid in um_slots:
            self._slots[sid].misses += 1

        for di in um_dets:
            det = dets[di]
            thumb = self._crop(frame, det["box"])
            name, name_conf = self._ocr.read_name(thumb)
            new_slot = SlotState(
                slot_id=self._next_slot_id,
                box=det["box"],
                class_name=det["cls"],
                conf=det["conf"],
                last_seen_frame=frame_idx,
                name_votes=[name] if name else [],
                name_final=name,
                name_conf=name_conf,
                last_ocr_frame=frame_idx,
                is_teacher=self._ocr.is_teacher(name),
            )
            self._slots[self._next_slot_id] = new_slot
            matches.append((self._next_slot_id, di))
            self._next_slot_id += 1

        # 오래된 슬롯 삭제
        for sid in list(self._slots.keys()):
            if self._slots[sid].misses > cfg.slot_max_misses:
                del self._slots[sid]
                self._pose_consec.pop(sid, None)

        # ── 캔버스 초기화 ─────────────────────────────────────────────────────
        canvas = np.zeros((frame_h, frame_w + cfg.info_box_w, 3), dtype=np.uint8)
        canvas[:, :frame_w] = frame
        canvas[:, frame_w:] = (20, 20, 20)
        cv2.putText(
            canvas,
            f"frame={frame_idx} t={ts:.1f}s dets={len(dets)} slots={len(matches)}",
            (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (220, 220, 220), 1, cv2.LINE_AA,
        )

        # ── 슬롯별 처리 ───────────────────────────────────────────────────────
        records: list[dict] = []
        for sid, di in sorted(matches, key=lambda x: x[0]):
            sl  = self._slots[sid]
            det = dets[di]

            # bbox 안정화
            det["box"] = tuple(map(int, stabilize_bbox(sl.box_smoothed, det["box"])))
            sl.box_smoothed = list(det["box"])
            sl.box = det["box"]
            sl.class_name = det["cls"]
            sl.conf = det["conf"]
            sl.last_seen_frame = frame_idx

            # 장기 miss 후 복귀 시 상태 리셋 (stale PERCLOS/raw_hist에 의한 false DROWSY 방지)
            if sl.misses >= cfg.noface_hold_frames:
                _reset_timers(sl, clear_perclos=True)
                sl.raw_hist.clear()
                sl.current_state = "NORMAL"
            sl.misses = 0

            x1, y1, x2, y2 = det["box"]
            thumb = self._crop(frame, det["box"])

            # 얼굴 특징 추출
            face_result = self._face_detector.detect(thumb, det["cls"])

            # NoFace 연속 카운터 업데이트
            prev_noface_long = sl.noface_consec >= cfg.noface_hold_frames
            if not face_result.lm_ok and not face_result.face_ok:
                sl.noface_consec += 1
            else:
                sl.noface_consec = 0
            is_noface = sl.noface_consec >= cfg.noface_hold_frames

            # 장기 No Face → 얼굴 복귀 시 상태 리셋 (stale PERCLOS에 의한 false DROWSY 방지)
            if prev_noface_long and not is_noface:
                _reset_timers(sl, clear_perclos=True)
                sl.raw_hist.clear()
                sl.current_state = "NORMAL"

            # Pose fallback: FaceMesh 랜드마크 검출 실패 시 고개 숙임 보조 감지
            if self._pose_detector is not None and not face_result.lm_ok:
                pose_result = self._pose_detector.detect(thumb)
                if pose_result is not None and pose_result.head_down:
                    self._pose_consec[sid] = self._pose_consec.get(sid, 0) + 1
                else:
                    self._pose_consec[sid] = max(0, self._pose_consec.get(sid, 0) - 1)
                face_result.pose_head_down = (
                    self._pose_consec.get(sid, 0) >= self._cfg.pose_consec_frames
                )
            else:
                self._pose_consec[sid] = max(0, self._pose_consec.get(sid, 0) - 1)

            # 모션
            curr_gray = cv2.cvtColor(thumb, cv2.COLOR_BGR2GRAY) if thumb.size > 0 else None
            motion = compute_motion(sl.prev_gray, curr_gray, face_result.face_box, thumb.shape)
            sl.prev_gray = curr_gray

            # 졸음 상태 업데이트
            raw_state, final_state, drowsy_reason = update_drowsiness_state(
                sl, face_result, motion, det["cls"], fps_eff, ts, cfg.drowsiness
            )
            update_baselines(sl, face_result, final_state, ts, cfg.drowsiness)

            sl.total_frames += 1
            if final_state == "DROWSY":   sl.frames_drowsy += 1
            elif final_state == "YAWN":   sl.frames_yawn   += 1
            elif final_state == "ABSENT": sl.frames_absent += 1
            else:                         sl.frames_normal += 1

            # OCR (필요할 때만)
            self._try_ocr(sl, thumb, frame_idx)

            # 시각화
            draw_slot_bbox(
                canvas, sid, det["box"], det["cls"], final_state, BOX_COLORS, STATE_COLORS,
                no_face=is_noface,
            )
            draw_face_box(canvas, (x1, y1), face_result.face_box)

            ibox_h = INFO_BOX_H
            if x2 + cfg.info_box_w <= canvas.shape[1]:
                ix = x2 + 2
            else:
                ix = max(0, x1 - (cfg.info_box_w - 4) - 2)
            iy = max(0, min(y1, canvas.shape[0] - ibox_h))

            draw_info_box(
                canvas, sl, face_result, (ix, iy),
                final_state, STATE_COLORS,
                box_w=cfg.info_box_w - 4,
                is_noface=is_noface,
            )

            records.append({
                "frame_idx":     frame_idx,
                "timestamp_s":   round(ts, 4),
                "slot_id":       sid,
                "name":          sl.name_final,
                "is_teacher":    int(sl.is_teacher),
                "final_state":   final_state,
                "raw_state":     raw_state,
                "drowsy_reason": drowsy_reason,
                "cls_name":      det["cls"],
                "cls_conf":      round(det["conf"], 4),
                "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                "lm_ok":         int(face_result.lm_ok),
                "face_ok":       int(face_result.face_ok),
                "ear":           face_result.ear,
                "mar":           face_result.mar,
                "pitch_like":    face_result.pitch_like,
                "tilt_deg":      face_result.tilt_deg,
                "face_center_y": face_result.face_center_y,
                "motion":        motion,
                "ear_low_f":     sl.ear_low_frames,
                "face_low_f":    sl.face_low_frames,
            })

        return canvas, records

    # ── 슬롯 요약 ─────────────────────────────────────────────────────────────

    def get_track_summary(self) -> list[dict]:
        """처리 완료 후 슬롯별 집계 요약을 반환합니다."""
        rows = []
        for sid in sorted(self._slots.keys()):
            sl = self._slots[sid]
            rows.append({
                "slot_id":       sid,
                "name":          sl.name_final,
                "name_conf":     round(sl.name_conf, 4),
                "total_frames":  sl.total_frames,
                "frames_normal": sl.frames_normal,
                "frames_drowsy": sl.frames_drowsy,
                "frames_yawn":   sl.frames_yawn,
                "frames_absent": sl.frames_absent,
                "bl_ear":        sl.bl_ear,
                "bl_pitch":      sl.bl_pitch,
                "bl_center_y":   sl.bl_center_y,
            })
        return rows

    # ── 내부 헬퍼 ─────────────────────────────────────────────────────────────

    def _yolo_detect(self, frame: np.ndarray) -> list[dict]:
        cfg = self._cfg
        results = self._model.predict(
            source=frame,
            imgsz=cfg.yolo_imgsz,
            conf=cfg.yolo_conf,
            iou=cfg.yolo_iou,
            max_det=cfg.yolo_max_det,
            verbose=False,
        )[0]
        dets: list[dict] = []
        if results.boxes is not None and len(results.boxes) > 0:
            for box, conf, cls_id in zip(
                results.boxes.xyxy.cpu().numpy(),
                results.boxes.conf.cpu().numpy(),
                results.boxes.cls.cpu().numpy().astype(int),
            ):
                x1, y1, x2, y2 = map(int, box.tolist())
                dets.append({
                    "box":  (x1, y1, x2, y2),
                    "conf": float(conf),
                    "cls":  results.names.get(int(cls_id), str(cls_id)),
                })
        return dets

    def _try_ocr(self, sl: SlotState, thumb: np.ndarray, frame_idx: int) -> None:
        """OCR 재시도 조건을 확인하고 필요하면 이름을 갱신합니다."""
        cfg = self._cfg
        ocr_interval = (
            cfg.ocr_fast_interval
            if frame_idx <= self._layout_boost_until
            else cfg.ocr_retry_interval
        )
        need_ocr = (
            (not sl.name_final or sl.name_conf < cfg.ocr_name_conf_lock)
            and (frame_idx - sl.last_ocr_frame >= ocr_interval)
        )
        if not need_ocr:
            return

        name, name_conf = self._ocr.read_name(thumb)
        if name:
            sl.name_votes.append(name)
            if len(sl.name_votes) > cfg.name_vote_maxlen:
                sl.name_votes = sl.name_votes[-cfg.name_vote_maxlen:]
            cnt = Counter(sl.name_votes)
            best, votes = cnt.most_common(1)[0]
            if votes >= cfg.ocr_lock_min_votes or (votes >= 2 and not sl.name_final):
                sl.name_final  = best
                sl.name_conf   = float(votes / len(sl.name_votes))
                sl.is_teacher  = self._ocr.is_teacher(sl.name_final)
        sl.last_ocr_frame = frame_idx

    @staticmethod
    def _crop(img: np.ndarray, box: tuple) -> np.ndarray:
        h, w = img.shape[:2]
        x1, y1, x2, y2 = box
        x1 = max(0, min(int(x1), w - 1)); y1 = max(0, min(int(y1), h - 1))
        x2 = max(x1 + 1, min(int(x2), w)); y2 = max(y1 + 1, min(int(y2), h))
        return img[y1:y2, x1:x2].copy()


# ─────────────────────────────────────────────────────────────────────────────
# 통합 실행 함수 (Jupyter/Script 호출용)
# ─────────────────────────────────────────────────────────────────────────────

def run_inference(
    input_path: str | Path = "data/video/TestVideo2.mp4",
    checkpoint: str | Path = "checkpoint/yolo11n/weights/best.pt",
    output_path: str | Path = "outputs/result.mp4",
    fps: float = 10.0,
    use_fallback: bool = True,
    teacher_names: Optional[list[str]] = None,
    start_sec: float = 0.0,
    end_sec: Optional[float] = None,
):
    """
    졸음 감지 파이프라인을 실행합니다.
    
    Args:
        input_path:    입력 영상 경로
        checkpoint:    YOLO 모델(.pt) 경로
        output_path:   결과 영상 저장 경로
        fps:           분석 목표 FPS
        use_fallback:  얼굴 인식 실패 시 Pose(고개 숙임) 감지 활성화 여부
        teacher_names: 강사 이름 리스트
        start_sec:     분석 시작 지점(초)
        end_sec:       분석 종료 지점(초)
    """
    load_env()
    
    # 경로 처리 (OpenCV는 문자열 경로를 선호합니다)
    checkpoint_str = str(checkpoint)
    input_str = str(input_path)
    output_str = str(output_path)
    
    output_path = Path(output_path)
    if output_path.is_dir():
        # 만약 폴더 경로가 들어왔다면 기본 파일명을 붙여줍니다.
        output_path = output_path / "result.mp4"
        output_str = str(output_path)
    
    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    frame_csv = output_dir / f"{output_path.stem}_frames.csv"
    track_csv = output_dir / f"{output_path.stem}_summary.csv"

    if not Path(checkpoint).exists():
        print(f"[경고] YOLO 체크포인트 없음: {checkpoint}")
    
    assert Path(input_path).exists(), f"입력 영상 없음: {input_path}"

    yolo_model = YOLO(checkpoint_str)

    config = PipelineConfig(
        teacher_names=teacher_names or ["강경미"],
        target_fps=fps,
        use_pose_fallback=use_fallback,
        start_sec=start_sec,
        end_sec=end_sec,
        drowsiness=DrowsinessConfig(
            ear_hold_strong_sec=0.5,
        ),
    )

    all_records = []
    track_summary = []

    with VideoReader(input_str, start_sec=config.start_sec,
                     end_sec=config.end_sec, target_fps=config.target_fps) as reader:

        canvas_w = reader.width + config.info_box_w

        with VideoWriter(output_str, reader.fps_effective,
                         canvas_w, reader.height) as writer:

            with ZoomPipeline(yolo_model, config) as pipeline:
                total = len(reader)
                pbar = tqdm(reader, total=total, desc=f"분석 중 ({Path(input_path).name})", unit="frame")
                
                for frame_idx, ts, frame in pbar:
                    canvas, records = pipeline.process_frame(frame, frame_idx, reader.fps, reader.fps_effective)
                    writer.write(canvas)
                    all_records.extend(records)
                    pbar.set_postfix({"ts": f"{ts:.1f}s", "dets": len(records)})

            track_summary = pipeline.get_track_summary()

    # CSV 저장
    if all_records:
        with open(frame_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer_csv = csv.DictWriter(f, fieldnames=list(all_records[0].keys()))
            writer_csv.writeheader()
            writer_csv.writerows(all_records)
        print(f"프레임 결과 저장: {frame_csv}")

    if track_summary:
        with open(track_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer_csv = csv.DictWriter(f, fieldnames=list(track_summary[0].keys()))
            writer_csv.writeheader()
            writer_csv.writerows(track_summary)
        print(f"수강생 요약 저장: {track_csv}")

    print(f"영상 저장 완료: {output_path}")
    return track_summary


# ─────────────────────────────────────────────────────────────────────────────
# 엔트리포인트 (CLI 실행)
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="졸음 감지 파이프라인 실행")
    parser.add_argument("--checkpoint", type=str, default="checkpoint/yolo11n/best.pt", help="YOLO 모델 경로")
    parser.add_argument("--input", type=str, required=True, help="입력 영상 경로")
    parser.add_argument("--output", type=str, default="outputs/result.mp4", help="결과 영상 저장 경로")
    parser.add_argument("--fps", type=float, default=10.0, help="분석 목표 FPS")
    parser.add_argument("--use_fallback", action="store_true", help="Pose fallback 활성화 여부")
    parser.add_argument("--teacher", type=str, default="강경미", help="강사 이름 (쉼표로 구분)")

    args = parser.parse_args()

    run_inference(
        input_path=args.input,
        checkpoint=args.checkpoint,
        output_path=args.output,
        fps=args.fps,
        use_fallback=args.use_fallback,
        teacher_names=args.teacher.split(","),
    )
