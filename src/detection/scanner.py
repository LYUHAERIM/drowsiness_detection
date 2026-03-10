from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

from .face import FaceDetector
from .metrics import mean_ear, mar, head_pose


def scan_frames(
    frames_dir: str | Path,
    glob_pattern: str = "**/*.jpg",
    max_faces: int = 1,
    min_detection_confidence: float = 0.5,
) -> pd.DataFrame:
    """
    프레임 이미지 디렉토리를 스캔해서 얼굴 검출 결과를 DataFrame으로 반환합니다.

    Args:
        frames_dir: 프레임 이미지가 있는 루트 디렉토리
        glob_pattern: 이미지 탐색 패턴 (기본: 하위 폴더 포함 jpg)
        max_faces: 최대 검출 얼굴 수
        min_detection_confidence: 얼굴 검출 최소 신뢰도

    Returns:
        DataFrame columns:
            - video_id: 상위 폴더명 (영상 ID)
            - filename: 파일명
            - path: 전체 경로
            - face_detected: 얼굴 검출 여부
            - ear: 평균 EAR (눈 종횡비)
            - mar: MAR (입 종횡비)
            - pitch: 고개 상하 각도
            - yaw: 고개 좌우 각도
    """
    frames_dir = Path(frames_dir)
    img_paths = sorted(frames_dir.glob(glob_pattern))

    if not img_paths:
        raise FileNotFoundError(f"이미지 없음: {frames_dir} / {glob_pattern}")

    rows = []
    with FaceDetector(max_faces=max_faces, min_detection_confidence=min_detection_confidence) as detector:
        for path in tqdm(img_paths, desc=f"스캔: {frames_dir.name}"):
            image = cv2.imread(str(path))
            result = detector.detect(image) if image is not None else None

            if result:
                _ear   = mean_ear(result.landmarks_px)
                _mar   = mar(result.landmarks_px)
                _pitch, _yaw = head_pose(result.landmarks)
            else:
                _ear = _mar = _pitch = _yaw = None

            rows.append({
                "video_id":      path.parent.name,
                "filename":      path.name,
                "path":          str(path),
                "face_detected": result is not None,
                "ear":           _ear,
                "mar":           _mar,
                "pitch":         _pitch,
                "yaw":           _yaw,
            })

    return pd.DataFrame(rows)
