from __future__ import annotations

import base64
import time
from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np

from src.detection.drowsiness import (
    DrowsinessConfig,
    compute_motion,
    update_baselines,
    update_drowsiness_state,
)
from src.detection.face import FaceMeshDetector
from src.tracking.slot import SlotState


@dataclass
class LiveInferenceResult:
    status: str
    alert: str
    report: str
    debug_text: str
    reason: str
    frame_received: bool
    frame_index: int


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


class LiveDrowsinessEngine:
    def __init__(self, fps: float = 5.0):
        self.fps = fps
        self.cfg = DrowsinessConfig()
        self.face_detector = FaceMeshDetector(
            min_detection_confidence=0.25,
            use_clahe=True,
        )

        self.slot = SlotState(
            slot_id=1,
            box=(0, 0, 0, 0),
            class_name="person_on",
            conf=1.0,
            last_seen_frame=0,
        )

        self.started_at = time.time()
        self.frame_count = 0
        self.last_reason = "init"

    def reset(self):
        self.slot = SlotState(
            slot_id=1,
            box=(0, 0, 0, 0),
            class_name="person_on",
            conf=1.0,
            last_seen_frame=0,
        )
        self.started_at = time.time()
        self.frame_count = 0
        self.last_reason = "reset"

    def close(self):
        self.face_detector.close()

    def analyze_data_url(self, data_url: str) -> LiveInferenceResult:
        frame = decode_data_url_to_bgr(data_url)
        return self.analyze_bgr(frame)

    def analyze_bgr(self, frame: Optional[np.ndarray]) -> LiveInferenceResult:
        if frame is None:
            return LiveInferenceResult(
                status="NORMAL",
                alert="프레임을 아직 받지 못했습니다.",
                report="실시간 카메라 프레임 대기 중",
                debug_text="frame=None",
                reason="frame_missing",
                frame_received=False,
                frame_index=self.frame_count,
            )

        self.frame_count += 1
        ts = time.time() - self.started_at

        h, w = frame.shape[:2]
        self.slot.box = (0, 0, w, h)
        self.slot.class_name = "person_on"
        self.slot.last_seen_frame = self.frame_count

        face_result = self.face_detector.detect(frame, cls_name="person_on")

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        motion = compute_motion(
            self.slot.prev_gray,
            gray,
            face_box=face_result.face_box,
            thumb_shape=gray.shape,
        )
        self.slot.prev_gray = gray

        raw_state, final_state, reason = update_drowsiness_state(
            slot=self.slot,
            face_result=face_result,
            motion=motion,
            cls_name="person_on",
            fps=self.fps,
            ts=ts,
            cfg=self.cfg,
        )
        self.last_reason = reason

        update_baselines(
            slot=self.slot,
            face_result=face_result,
            final_state=final_state,
            ts=ts,
            cfg=self.cfg,
        )

        self._update_stats(final_state)

        alert_map = {
            "NORMAL": "이상 없음",
            "DROWSY": "졸음 감지 알림",
            "ABSENT": "자리 이탈 알림",
            "IGNORE": "분석 제외 상태",
        }
        alert = alert_map.get(final_state, "상태를 확인할 수 없습니다")

        report = (
            f"총 프레임: {self.frame_count}\n"
            f"NORMAL: {self.slot.frames_normal}\n"
            f"DROWSY: {self.slot.frames_drowsy}\n"
            f"ABSENT: {self.slot.frames_absent}\n"
            f"최근 reason: {self.last_reason}"
        )

        debug_text = (
            f"raw={raw_state}, final={final_state}, " f"ear={face_result.ear:.4f} "
            if not np.isnan(face_result.ear)
            else f"raw={raw_state}, final={final_state}, ear=nan "
        )
        debug_text += (
            f"mar={face_result.mar:.4f} "
            if not np.isnan(face_result.mar)
            else "mar=nan "
        )
        debug_text += (
            f"pitch={face_result.pitch_like:.4f} "
            if not np.isnan(face_result.pitch_like)
            else "pitch=nan "
        )
        debug_text += (
            f"center_y={face_result.face_center_y:.4f} "
            if not np.isnan(face_result.face_center_y)
            else "center_y=nan "
        )
        debug_text += f"motion={motion:.4f}" if not np.isnan(motion) else "motion=nan"

        return LiveInferenceResult(
            status=final_state,
            alert=alert,
            report=report,
            debug_text=debug_text,
            reason=self.last_reason,
            frame_received=True,
            frame_index=self.frame_count,
        )

    def _update_stats(self, final_state: str):
        self.slot.total_frames += 1
        if final_state == "NORMAL":
            self.slot.frames_normal += 1
        elif final_state == "DROWSY":
            self.slot.frames_drowsy += 1
        elif final_state == "ABSENT":
            self.slot.frames_absent += 1
