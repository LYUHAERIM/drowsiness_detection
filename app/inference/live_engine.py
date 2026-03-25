import base64
import logging
import os
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

import cv2
import numpy as np

from src.detection.drowsiness import (
    DrowsinessConfig,
    compute_motion,
    update_baselines,
    update_drowsiness_state,
)
from src.detection.face import FaceMeshDetector, FaceMeshResult
from src.ocr.reader import NameOCR
from src.tracking.slot import (
    SlotState,
    match_slots_to_detections,
    sort_detections_reading_order,
    stabilize_bbox,
)
from src.visual.annotator import draw_text_bg

LOGGER = logging.getLogger(__name__)


def _empty_face_result() -> FaceMeshResult:
    nan = float("nan")
    return FaceMeshResult(
        lm_ok=False,
        face_ok=False,
        ear=nan,
        mar=nan,
        pitch_like=nan,
        tilt_deg=nan,
        face_center_y=nan,
        face_box=None,
    )


class _FallbackFaceDetector:
    def detect(
        self, _thumb_bgr: np.ndarray, cls_name: str = "person_on"
    ) -> FaceMeshResult:
        return _empty_face_result()

    def close(self):
        return None


@dataclass
class LiveInferenceResult:
    status: str
    alert: str
    report: str
    debug_text: str
    reason: str
    frame_received: bool
    frame_index: int
    students: list[dict] = field(default_factory=list)
    overlay_data_url: str = ""


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
        LOGGER.exception("Failed to decode data url frame")
        return None


def encode_bgr_to_data_url(frame: np.ndarray, quality: int = 85) -> str:
    ok, encoded = cv2.imencode(
        ".jpg",
        frame,
        [int(cv2.IMWRITE_JPEG_QUALITY), int(quality)],
    )
    if not ok:
        return ""
    payload = base64.b64encode(encoded.tobytes()).decode("ascii")
    return f"data:image/jpeg;base64,{payload}"


class MultiStudentEngine:
    def __init__(self, fps: float = 5.0):
        self.fps = fps
        self.cfg = DrowsinessConfig()
        self.max_students = 5
        self.detect_interval = 3
        self.ocr_interval = 15
        self.max_slot_misses = max(3, int(round(fps * 2.0)))
        self.model_name = os.getenv(
            "DROWSINESS_YOLO_MODEL", "checkpoint/yolo11n/weights/best.pt"
        )

        self.face_detector = None
        self.name_reader = None
        self.yolo_model = None
        self._face_detector_attempted = False
        self._name_reader_attempted = False
        self._yolo_attempted = False

        self.started_at = time.time()
        self.frame_count = 0
        self.next_slot_id = 1
        self.last_reason = "init"
        self.last_detection_debug = "detect=waiting"
        self.last_detections: list[dict] = []
        self.slots: dict[int, SlotState] = {}

    def _build_name_reader(self) -> Optional[NameOCR]:
        try:
            return NameOCR(gpu=False)
        except Exception:
            LOGGER.exception("OCR reader disabled")
            return None

    def _build_yolo_model(self):
        try:
            from ultralytics import YOLO

            model = YOLO(self.model_name)
            LOGGER.info("Loaded YOLO model: %s", self.model_name)
            return model
        except Exception:
            LOGGER.exception("YOLO model disabled: %s", self.model_name)
            return None

    def reset(self):
        self._ensure_runtime_components()
        self.started_at = time.time()
        self.frame_count = 0
        self.next_slot_id = 1
        self.last_reason = "reset"
        self.last_detection_debug = "detect=reset"
        self.last_detections = []
        self.slots = {}

    def close(self):
        if self.face_detector is not None:
            self.face_detector.close()

    def _ensure_runtime_components(self) -> None:
        if self.face_detector is None and not self._face_detector_attempted:
            self._face_detector_attempted = True
            try:
                self.face_detector = FaceMeshDetector(
                    min_detection_confidence=0.25,
                    use_clahe=True,
                )
            except Exception:
                LOGGER.exception("Face detector disabled")
                self.face_detector = _FallbackFaceDetector()
        if self.name_reader is None and not self._name_reader_attempted:
            self._name_reader_attempted = True
            self.name_reader = self._build_name_reader()
        if self.yolo_model is None and not self._yolo_attempted:
            self._yolo_attempted = True
            self.yolo_model = self._build_yolo_model()

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
                students=[],
                overlay_data_url="",
            )

        self.frame_count += 1
        self._ensure_runtime_components()
        ts = time.time() - self.started_at

        detections = self._get_detections(frame)
        self._update_slots(frame, detections)

        student_rows: list[dict] = []
        for slot_id in list(self.slots.keys()):
            slot = self.slots[slot_id]
            student_rows.append(self._run_slot_inference(frame, slot, ts))

        student_rows.sort(key=lambda row: row["id"])
        summary_status = self._summarize_status(student_rows)
        alert = self._build_alert_text(student_rows)
        report = self._build_report_text(student_rows)
        debug_text = self._build_debug_text(student_rows)
        overlay_data_url = self._render_overlay_frame(frame, detections, student_rows)

        return LiveInferenceResult(
            status=summary_status,
            alert=alert,
            report=report,
            debug_text=debug_text,
            reason=self.last_reason,
            frame_received=True,
            frame_index=self.frame_count,
            students=student_rows,
            overlay_data_url=overlay_data_url,
        )

    def _get_detections(self, frame: np.ndarray) -> list[dict]:
        should_detect = (
            self.frame_count == 1
            or self.frame_count % self.detect_interval == 0
            or not self.last_detections
        )
        if not should_detect:
            self.last_detection_debug = (
                f"detect=cached count={len(self.last_detections)}"
            )
            return list(self.last_detections)

        detections = self._run_yolo_detection(frame)
        detections = sort_detections_reading_order(detections)[: self.max_students]
        self.last_detections = detections
        self.last_detection_debug = f"detect=run count={len(detections)}"
        return detections

    def _run_yolo_detection(self, frame: np.ndarray) -> list[dict]:
        if self.yolo_model is None:
            h, w = frame.shape[:2]
            LOGGER.debug("YOLO unavailable, falling back to a full-frame slot")
            return [{"box": (0, 0, w, h), "cls": "person_on", "conf": 0.0}]

        try:
            results = self.yolo_model.predict(
                source=frame,
                conf=0.25,
                iou=0.45,
                verbose=False,
            )
        except Exception:
            LOGGER.exception("YOLO inference failed, using cached detections")
            return list(self.last_detections)

        if not results:
            return []

        dets: list[dict] = []
        boxes = results[0].boxes
        if boxes is None:
            return dets

        for box in boxes:
            xyxy = box.xyxy[0].tolist()
            x1, y1, x2, y2 = [int(v) for v in xyxy]
            if x2 <= x1 or y2 <= y1:
                continue
            dets.append(
                {
                    "box": (x1, y1, x2, y2),
                    "cls": "person_on",
                    "conf": float(box.conf[0].item()) if box.conf is not None else 0.0,
                    "label": self._yolo_label_name(box),
                }
            )
        return dets

    def _yolo_label_name(self, box) -> str:
        try:
            cls_idx = int(box.cls[0].item())
            return str(self.yolo_model.names.get(cls_idx, cls_idx))
        except Exception:
            return "student"

    def _update_slots(self, frame: np.ndarray, detections: list[dict]) -> None:
        _, frame_w = frame.shape[:2]
        frame_h = frame.shape[0]
        matches, unmatched_slots, unmatched_dets = match_slots_to_detections(
            self.slots,
            detections,
            frame_w=frame_w,
            frame_h=frame_h,
        )

        for slot_id, det_idx in matches:
            det = detections[det_idx]
            slot = self.slots[slot_id]
            slot.box_smoothed = stabilize_bbox(slot.box_smoothed, det["box"])
            slot.box = tuple(int(v) for v in slot.box_smoothed)
            slot.class_name = det["cls"]
            slot.conf = det["conf"]
            slot.last_seen_frame = self.frame_count
            slot.misses = 0

        # TODO: 레이아웃 변경이 큰 경우 슬롯 전체 리셋 정책을 추가할 수 있습니다.
        for slot_id in unmatched_slots:
            slot = self.slots[slot_id]
            slot.misses += 1
            if slot.misses > self.max_slot_misses:
                del self.slots[slot_id]
                continue
            slot.class_name = "person_off"

        for det_idx in unmatched_dets:
            if len(self.slots) >= self.max_students:
                break
            det = detections[det_idx]
            slot_id = self._allocate_slot_id()
            self.slots[slot_id] = SlotState(
                slot_id=slot_id,
                box=det["box"],
                class_name=det["cls"],
                conf=det["conf"],
                last_seen_frame=self.frame_count,
                box_smoothed=list(det["box"]),
            )

    def _allocate_slot_id(self) -> int:
        while self.next_slot_id in self.slots:
            self.next_slot_id += 1
        slot_id = self.next_slot_id
        self.next_slot_id += 1
        return slot_id

    def _run_slot_inference(
        self, frame: np.ndarray, slot: SlotState, ts: float
    ) -> dict:
        crop = self._crop_bbox(frame, slot.box)
        if crop is None:
            slot.class_name = "person_off"
            raw_state, final_state, reason = update_drowsiness_state(
                slot=slot,
                face_result=_empty_face_result(),
                motion=float("nan"),
                cls_name="person_off",
                fps=self.fps,
                ts=ts,
                cfg=self.cfg,
            )
            self.last_reason = reason
            self._update_slot_stats(slot, final_state)
            return self._student_row(slot, raw_state, final_state, reason)

        cls_name = slot.class_name if slot.misses == 0 else "person_off"
        face_result = self.face_detector.detect(crop, cls_name=cls_name)

        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        motion = compute_motion(
            slot.prev_gray,
            gray,
            face_box=face_result.face_box,
            thumb_shape=gray.shape,
        )
        slot.prev_gray = gray

        raw_state, final_state, reason = update_drowsiness_state(
            slot=slot,
            face_result=face_result,
            motion=motion,
            cls_name=cls_name,
            fps=self.fps,
            ts=ts,
            cfg=self.cfg,
        )
        self.last_reason = reason

        update_baselines(
            slot=slot,
            face_result=face_result,
            final_state=final_state,
            ts=ts,
            cfg=self.cfg,
        )

        if cls_name == "person_on":
            self._maybe_update_name(slot, crop)

        self._update_slot_stats(slot, final_state)
        return self._student_row(slot, raw_state, final_state, reason)

    def _crop_bbox(self, frame: np.ndarray, box: tuple) -> Optional[np.ndarray]:
        h, w = frame.shape[:2]
        x1, y1, x2, y2 = [int(v) for v in box]
        x1 = max(0, min(w, x1))
        y1 = max(0, min(h, y1))
        x2 = max(0, min(w, x2))
        y2 = max(0, min(h, y2))
        if x2 <= x1 or y2 <= y1:
            return None
        return frame[y1:y2, x1:x2].copy()

    def _maybe_update_name(self, slot: SlotState, crop: np.ndarray) -> None:
        if self.name_reader is None:
            return
        should_run_ocr = (
            not slot.name_final
            or self.frame_count - slot.last_ocr_frame >= self.ocr_interval
        )
        if not should_run_ocr:
            return

        slot.last_ocr_frame = self.frame_count
        try:
            name, conf = self.name_reader.read_name(crop)
        except Exception:
            LOGGER.exception("OCR failed for slot %s", slot.slot_id)
            return

        if not name:
            return

        slot.name_votes.append(name)
        recent_votes = slot.name_votes[-10:]
        best_name, votes = Counter(recent_votes).most_common(1)[0]
        slot.name_final = best_name
        slot.name_conf = max(slot.name_conf, conf, votes / max(len(recent_votes), 1))
        slot.is_teacher = self.name_reader.is_teacher(best_name)

    def _update_slot_stats(self, slot: SlotState, final_state: str) -> None:
        slot.total_frames += 1
        if final_state == "NORMAL":
            slot.frames_normal += 1
        elif final_state == "DROWSY":
            slot.frames_drowsy += 1
        elif final_state == "ABSENT":
            slot.frames_absent += 1

    def _student_row(
        self, slot: SlotState, raw_state: str, final_state: str, reason: str
    ) -> dict:
        return {
            "id": slot.slot_id,
            "name": slot.name_final or f"학생 {slot.slot_id}",
            "status": final_state,
            "raw_status": raw_state,
            "reason": reason,
            "bbox": list(slot.box),
            "present": slot.class_name == "person_on" and slot.misses == 0,
            "name_conf": round(float(slot.name_conf), 3),
            "conf": round(float(slot.conf), 3),
            "class_name": slot.class_name,
            "misses": int(slot.misses),
        }

    def _summarize_status(self, students: list[dict]) -> str:
        if any(student["status"] == "DROWSY" for student in students):
            return "DROWSY"
        if any(student["status"] == "ABSENT" for student in students):
            return "ABSENT"
        return "NORMAL"

    def _build_alert_text(self, students: list[dict]) -> str:
        drowsy = [
            student["name"] for student in students if student["status"] == "DROWSY"
        ]
        absent = [
            student["name"] for student in students if student["status"] == "ABSENT"
        ]
        if drowsy:
            return f"졸음 감지: {', '.join(drowsy[:3])}"
        if absent:
            return f"자리 이탈 감지: {', '.join(absent[:3])}"
        if students:
            return f"총 {len(students)}명 분석 중"
        return f"감지된 학생이 없습니다. {self.last_detection_debug}"

    def _build_report_text(self, students: list[dict]) -> str:
        lines = [
            f"총 프레임: {self.frame_count}",
            f"추적 학생 수: {len(students)}",
        ]
        for student in students:
            lines.append(
                f"ID {student['id']} {student['name']}: {student['status']} "
                f"(reason={student['reason'] or '-'})"
            )
        return "\n".join(lines)

    def _build_debug_text(self, students: list[dict]) -> str:
        student_bits = [
            (
                f"id={student['id']}:{student['status']}/{student['reason'] or '-'} "
                f"box={student['bbox']} conf={student['conf']:.2f} "
                f"miss={student['misses']}"
            )
            for student in students
        ]
        return (
            f"{self.last_detection_debug} slots={len(self.slots)} "
            f"tracked={len(students)} model={self.model_name}\n"
            + " | ".join(student_bits)
        ).strip()

    def _render_overlay_frame(
        self,
        frame: np.ndarray,
        detections: list[dict],
        students: list[dict],
    ) -> str:
        """
        현재 추론 프레임 위에 raw detection 과 tracked slot 을 함께 그립니다.

        - raw detection: 얇은 파란 박스
        - tracked slot: 상태 기반 두꺼운 박스
        """
        canvas = frame.copy()

        for det_idx, det in enumerate(detections, start=1):
            self._draw_raw_detection(canvas, det_idx, det)

        for student in students:
            self._draw_tracked_slot(canvas, student)

        return encode_bgr_to_data_url(canvas)

    def _draw_raw_detection(self, canvas: np.ndarray, det_idx: int, det: dict) -> None:
        x1, y1, x2, y2 = [int(v) for v in det["box"]]
        raw_color = (255, 0, 0)
        cv2.rectangle(canvas, (x1, y1), (x2, y2), raw_color, 1, cv2.LINE_AA)
        label = f"DET{det_idx} {det.get('label', 'student')} {det.get('conf', 0.0):.2f}"
        self._draw_label(canvas, label, (x1, max(18, y1 - 6)), raw_color)

    def _draw_tracked_slot(self, canvas: np.ndarray, student: dict) -> None:
        x1, y1, x2, y2 = [int(v) for v in student["bbox"]]
        status = student.get("status") or "NORMAL"
        slot_color = self._status_color(status)

        # tracked slot 은 raw detection 보다 눈에 띄게 굵게 그립니다.
        cv2.rectangle(canvas, (x1, y1), (x2, y2), slot_color, 3, cv2.LINE_AA)

        label_parts = [
            f"S{student['id']}",
            status,
            f"{student.get('conf', 0.0):.2f}",
        ]
        name = student.get("name") or ""
        if name:
            label_parts.append(name)
        label = " | ".join(label_parts)
        self._draw_label(canvas, label, (x1, min(canvas.shape[0] - 6, y2 + 18)), slot_color)

    def _draw_label(self, canvas: np.ndarray, text: str, origin: tuple[int, int], color: tuple[int, int, int]) -> None:
        try:
            draw_text_bg(
                canvas,
                text=text,
                org=origin,
                scale=0.5,
                color=(255, 255, 255),
                bg=color,
                thickness=1,
                pad=3,
            )
        except Exception:
            x, y = origin
            cv2.putText(
                canvas,
                text,
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                color,
                1,
                cv2.LINE_AA,
            )

    def _status_color(self, status: str) -> tuple[int, int, int]:
        if status == "DROWSY":
            return (40, 40, 255)
        if status == "ABSENT":
            return (0, 215, 255)
        return (60, 200, 60)


LiveDrowsinessEngine = MultiStudentEngine
