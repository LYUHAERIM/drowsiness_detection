import urllib.request
import cv2
import numpy as np
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

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
