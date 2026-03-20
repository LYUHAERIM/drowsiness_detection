import math
import urllib.request
import cv2
import numpy as np
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

from .metrics import ear as _metrics_ear, mar as _metrics_mar

# face_landmarker.task 모델 자동 다운로드
_MODEL_PATH = Path(__file__).parent / "face_landmarker.task"
_MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "face_landmarker/face_landmarker/float16/1/face_landmarker.task"
)


def _ensure_model() -> str:
    if not _MODEL_PATH.exists():
        print(f"모델 다운로드 중: {_MODEL_URL}")
        urllib.request.urlretrieve(_MODEL_URL, _MODEL_PATH)
        print(f"저장 완료: {_MODEL_PATH}")
    return str(_MODEL_PATH)


@dataclass
class FaceResult:
    """얼굴 검출 결과"""
    landmarks: np.ndarray    # (478, 3) - 정규화 좌표 (x, y, z)
    landmarks_px: np.ndarray  # (478, 2) - 픽셀 좌표 (x, y)


class FaceDetector:
    """MediaPipe FaceLandmarker 기반 얼굴 랜드마크 검출기 (Tasks API)"""

    def __init__(
        self,
        max_faces: int = 1,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        options = vision.FaceLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=_ensure_model()),
            num_faces=max_faces,
            min_face_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            running_mode=vision.RunningMode.IMAGE,
        )
        self._detector = vision.FaceLandmarker.create_from_options(options)

    def detect(self, image: np.ndarray) -> Optional[FaceResult]:
        """
        이미지에서 첫 번째 얼굴 랜드마크를 검출합니다.

        Args:
            image: BGR numpy 배열

        Returns:
            FaceResult (검출 성공) 또는 None (검출 실패)
        """
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self._detector.detect(mp_image)

        if not result.face_landmarks:
            return None

        h, w = image.shape[:2]
        lm = result.face_landmarks[0]

        landmarks = np.array([[p.x, p.y, p.z] for p in lm], dtype=np.float32)
        landmarks_px = (landmarks[:, :2] * [w, h]).astype(np.int32)

        return FaceResult(landmarks=landmarks, landmarks_px=landmarks_px)

    def is_valid(self, image: np.ndarray) -> bool:
        """얼굴이 검출되면 True"""
        return self.detect(image) is not None

    def close(self):
        self._detector.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


# ─────────────────────────────────────────────────────────────────────────────
# FaceMeshDetector  (legacy API + FaceDetection fallback)
# v6 파이프라인에서 사용하는 고급 특징 추출기
# ─────────────────────────────────────────────────────────────────────────────

# MediaPipe legacy FaceMesh 랜드마크 인덱스
_LEFT_EYE_IDX   = [33, 160, 158, 133, 153, 144]
_RIGHT_EYE_IDX  = [362, 385, 387, 263, 373, 380]
_NOSE_TIP_IDX   = 1
_CHIN_IDX       = 152
_L_EYE_OUT_IDX  = 33
_R_EYE_OUT_IDX  = 263
_MOUTH_TOP_IDX  = 13
_MOUTH_BOT_IDX  = 14
_MOUTH_LEFT_IDX = 78
_MOUTH_RIGHT_IDX = 308


@dataclass
class FaceMeshResult:
    """
    FaceMeshDetector 특징 추출 결과.

    Attributes:
        lm_ok:        FaceMesh 랜드마크 검출 성공 여부
        face_ok:      얼굴 영역 확인 여부 (lm_ok 또는 FaceDetection fallback)
        ear:          Eye Aspect Ratio (낮을수록 눈 감김)
        mar:          Mouth Aspect Ratio (높을수록 입 벌림)
        pitch_like:   코↔눈중심↔턱 비율 기반 고개 숙임 추정
        tilt_deg:     눈 기울기 각도 (degree)
        face_center_y: 얼굴 bbox 중심 y 좌표 (이미지 높이 기준 0~1)
        face_box:     (x1, y1, x2, y2) 원본 썸네일 좌표, None이면 미검출
    """
    lm_ok: bool
    face_ok: bool
    ear: float
    mar: float
    pitch_like: float
    tilt_deg: float
    face_center_y: float
    face_box: Optional[tuple]
    pose_head_down: bool = False  # Pose fallback 고개 숙임 감지 결과


class FaceMeshDetector:
    """
    MediaPipe legacy FaceMesh + FaceDetection 기반 얼굴 특징 추출기.

    FaceLandmarker (Tasks API) 기반으로 EAR, MAR, pitch_like, tilt_deg,
    face_center_y를 한 번에 반환합니다.

    CLAHE 전처리로 어두운 환경 대응. 특징 추출 로직을 바꾸려면
    이 클래스만 수정하면 됩니다.

    Args:
        min_detection_confidence: 검출 최소 신뢰도
        min_tracking_confidence: 트래킹 최소 신뢰도
        use_clahe: CLAHE 밝기 보정 사용 여부
    """

    def __init__(
        self,
        min_detection_confidence: float = 0.25,
        min_tracking_confidence: float = 0.25,
        use_clahe: bool = True,
    ):
        options = vision.FaceLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=_ensure_model()),
            num_faces=1,
            min_face_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            running_mode=vision.RunningMode.IMAGE,
        )
        self._detector = vision.FaceLandmarker.create_from_options(options)
        self._use_clahe = use_clahe
        self._clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    # ── 전처리 ────────────────────────────────────────────────────────────────

    def _enhance(self, bgr: np.ndarray) -> tuple[np.ndarray, float]:
        """업스케일 + CLAHE 전처리. (처리 이미지, 스케일 비율) 반환."""
        h, w = bgr.shape[:2]
        scale = 2.0 if max(h, w) < 200 else 1.5
        up = cv2.resize(bgr, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        if self._use_clahe:
            lab = cv2.cvtColor(up, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            up = cv2.cvtColor(cv2.merge([self._clahe.apply(l), a, b]), cv2.COLOR_LAB2BGR)
        return up, scale

    # ── 메인 검출 ─────────────────────────────────────────────────────────────

    def detect(self, thumb_bgr: np.ndarray, cls_name: str = "person_on") -> FaceMeshResult:
        """
        YOLO crop 이미지에서 얼굴 특징을 추출합니다.

        Args:
            thumb_bgr: BGR 이미지 (YOLO bounding box crop)
            cls_name:  YOLO 클래스명 ("person_on"이 아니면 빈 결과 반환)

        Returns:
            FaceMeshResult
        """
        _nan = float("nan")
        empty = FaceMeshResult(
            lm_ok=False, face_ok=False,
            ear=_nan, mar=_nan, pitch_like=_nan,
            tilt_deg=_nan, face_center_y=_nan, face_box=None,
        )

        if cls_name != "person_on":
            return empty

        h0, w0 = thumb_bgr.shape[:2]
        if h0 < 15 or w0 < 15:
            return empty

        up, scale = self._enhance(thumb_bgr)
        h, w = up.shape[:2]
        rgb = cv2.cvtColor(up, cv2.COLOR_BGR2RGB)

        ear = mar = pitch_like = tilt_deg = _nan
        face_box = None
        lm_ok = False

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self._detector.detect(mp_image)
        if result.face_landmarks:
            lm_ok = True
            lm = result.face_landmarks[0]

            # 정규화 좌표 → 픽셀 좌표 배열 (float32, shape: N×2)
            lm_px = np.array([[p.x * w, p.y * h] for p in lm], dtype=np.float32)

            # EAR / MAR: metrics.py 공용 함수 재사용
            ear = (_metrics_ear(lm_px, _LEFT_EYE_IDX) + _metrics_ear(lm_px, _RIGHT_EYE_IDX)) / 2.0
            mar = _metrics_mar(lm_px)

            # pitch_like / tilt_deg
            nose    = lm_px[_NOSE_TIP_IDX]
            chin    = lm_px[_CHIN_IDX]
            le_pt   = lm_px[_L_EYE_OUT_IDX]
            re_pt   = lm_px[_R_EYE_OUT_IDX]
            eye_mid = (le_pt + re_pt) / 2.0

            pitch_like = float((nose[1] - eye_mid[1]) / (chin[1] - eye_mid[1] + 1e-6))
            dy = re_pt[1] - le_pt[1]
            dx = re_pt[0] - le_pt[0] + 1e-6
            tilt_deg = abs(math.degrees(math.atan2(dy, dx)))

            # face_box
            xs, ys = lm_px[:, 0], lm_px[:, 1]
            face_box = (
                max(0, int(xs.min() / scale)), max(0, int(ys.min() / scale)),
                min(w0, int(xs.max() / scale)), min(h0, int(ys.max() / scale)),
            )

        face_center_y = _nan
        face_ok = False

        if lm_ok and face_box:
            _, fy1, _, fy2 = face_box
            face_center_y = ((fy1 + fy2) / 2.0) / h0
            face_ok = True

        return FaceMeshResult(
            lm_ok=lm_ok, face_ok=face_ok,
            ear=float(ear), mar=float(mar),
            pitch_like=float(pitch_like), tilt_deg=float(tilt_deg),
            face_center_y=float(face_center_y),
            face_box=face_box,
        )

    def close(self):
        self._detector.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
