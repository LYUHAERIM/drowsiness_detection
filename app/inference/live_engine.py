from __future__ import annotations

import base64
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import torch
from ultralytics import YOLO

from scripts.infer_video import PipelineConfig, ZoomPipeline


@dataclass
class SlotInfo:
    slot_id: int
    name: str
    status: str
    class_name: str
    is_teacher: bool
    ear: float
    mar: float
    box_pct: tuple = field(default_factory=lambda: (0.0, 0.0, 0.0, 0.0))  # (x1%, y1%, x2%, y2%)
    noface: bool = False


@dataclass
class LiveInferenceResult:
    slots: list[SlotInfo]
    status: str           # 대표 상태 (DROWSY 우선, 없으면 NORMAL)
    alert: str
    report: str
    debug_text: str
    frame_received: bool
    frame_index: int
    annotated_frame: Optional[np.ndarray] = None


def decode_data_url_to_bgr(data_url: str) -> Optional[np.ndarray]:
    if not data_url or "," not in data_url:
        return None
    try:
        encoded = data_url.split(",", 1)[1]
        image_bytes = base64.b64decode(encoded)
        np_arr = np.frombuffer(image_bytes, dtype=np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return frame
    except Exception:
        return None


def _select_device() -> int | str:
    if torch.cuda.is_available():
        return 0
    try:
        mps_available = getattr(getattr(torch, "backends", None), "mps", None)
        if mps_available is not None and mps_available.is_available():
            return "mps"
    except Exception:
        pass
    return "cpu"


class LiveZoomEngine:
    """ZoomPipeline을 실시간 Gradio 추론에 사용하는 엔진."""

    def __init__(self, checkpoint_path: str | Path, fps: float = 5.0):
        self.fps = fps
        self._checkpoint_path = str(checkpoint_path)

        device = _select_device()
        self._model = YOLO(self._checkpoint_path)
        self._model.to(device if isinstance(device, str) else f"cuda:{device}")

        self._config = PipelineConfig(
            target_fps=fps,
            device=device,
            ocr_retry_interval=30,   # 90 → 30: 6초마다 재시도 (fps=5 기준)
            ocr_fast_interval=5,     # 20 → 5: 시작 직후 1초마다
        )
        self._pipeline: Optional[ZoomPipeline] = None
        self._open_pipeline()

        self.started_at = time.time()
        self.frame_count = 0

    def _open_pipeline(self) -> None:
        if self._pipeline is not None:
            try:
                self._pipeline.close()
            except Exception:
                pass
        self._pipeline = ZoomPipeline(self._model, self._config)
        self._pipeline.open()

    def reset(self) -> None:
        self._open_pipeline()
        self.started_at = time.time()
        self.frame_count = 0

    def close(self) -> None:
        if self._pipeline is not None:
            try:
                self._pipeline.close()
            except Exception:
                pass
            self._pipeline = None

    def analyze_data_url(self, data_url: str) -> LiveInferenceResult:
        frame = decode_data_url_to_bgr(data_url)
        return self.analyze_bgr(frame)

    def analyze_bgr(self, frame: Optional[np.ndarray]) -> LiveInferenceResult:
        if frame is None:
            return LiveInferenceResult(
                slots=[],
                status="NORMAL",
                alert="프레임을 아직 받지 못했습니다.",
                report="실시간 카메라 프레임 대기 중",
                debug_text="frame=None",
                frame_received=False,
                frame_index=self.frame_count,
            )

        self.frame_count += 1

        canvas, records = self._pipeline.process_frame(
            frame,
            frame_idx=self.frame_count,
            fps=self.fps,
        )

        # records → SlotInfo 목록으로 변환
        frame_h, frame_w = frame.shape[:2]
        MIN_BBOX_W, MIN_BBOX_H = 100, 100  # 1920x1080 기준 최소 bbox 크기

        slots: list[SlotInfo] = []
        for r in records:
            ear = r.get("ear", float("nan"))
            mar = r.get("mar", float("nan"))
            x1, y1, x2, y2 = r.get("x1", 0), r.get("y1", 0), r.get("x2", 0), r.get("y2", 0)
            bw, bh = x2 - x1, y2 - y1
            box_pct = (x1 / frame_w, y1 / frame_h, x2 / frame_w, y2 / frame_h)

            status = r["final_state"]
            # bbox가 너무 작으면 FaceMesh 결과를 신뢰할 수 없으므로 NORMAL 처리
            if not bool(r.get("is_teacher", 0)) and (bw < MIN_BBOX_W or bh < MIN_BBOX_H):
                status = "NORMAL"

            noface = not bool(r.get("lm_ok", 1)) and not bool(r.get("face_ok", 1))

            slots.append(SlotInfo(
                slot_id=r["slot_id"],
                name=r["name"] or f"학생 {r['slot_id']}",
                status=status,
                class_name=r["cls_name"],
                is_teacher=bool(r.get("is_teacher", 0)),
                ear=ear if not (isinstance(ear, float) and np.isnan(ear)) else 0.0,
                mar=mar if not (isinstance(mar, float) and np.isnan(mar)) else 0.0,
                box_pct=box_pct,
                noface=noface,
            ))

        # 대표 상태: DROWSY > YAWN > ABSENT > NORMAL
        priority = {"DROWSY": 3, "YAWN": 2, "ABSENT": 1, "NORMAL": 0}
        rep_status = "NORMAL"
        if slots:
            rep_status = max(
                (s.status for s in slots if not s.is_teacher),
                key=lambda x: priority.get(x, 0),
                default="NORMAL",
            )

        alert_map = {
            "NORMAL": "이상 없음",
            "DROWSY": "졸음 감지 알림",
            "YAWN": "하품 감지",
            "ABSENT": "자리 이탈 알림",
        }
        alert = alert_map.get(rep_status, "상태를 확인할 수 없습니다")

        student_slots = [s for s in slots if not s.is_teacher]
        drowsy_names = [s.name for s in student_slots if s.status == "DROWSY"]
        absent_names = [s.name for s in student_slots if s.status == "ABSENT"]

        report_lines = [f"총 프레임: {self.frame_count}", f"감지된 슬롯: {len(slots)}명"]
        if drowsy_names:
            report_lines.append(f"졸음: {', '.join(drowsy_names)}")
        if absent_names:
            report_lines.append(f"이탈: {', '.join(absent_names)}")

        slot_debug = " | ".join(
            f"[{s.slot_id}]{s.name}={s.status}" for s in slots
        )
        debug_text = f"frame={self.frame_count} slots={len(slots)} {slot_debug}"

        return LiveInferenceResult(
            slots=slots,
            status=rep_status,
            alert=alert,
            report="\n".join(report_lines),
            debug_text=debug_text,
            frame_received=True,
            frame_index=self.frame_count,
            annotated_frame=canvas,
        )
