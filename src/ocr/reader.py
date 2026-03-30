"""
EasyOCR 기반 Zoom 썸네일 이름 추출기.

썸네일 하단 이름 표시 영역을 크롭해 OCR로 이름을 읽고,
다수결 투표로 최종 이름을 확정합니다.
"""
import re
from collections import Counter
from typing import Optional

import cv2
import numpy as np
from src.teacher import is_teacher_name, normalize_person_name, resolve_teacher_names


def _normalize_name(text: Optional[str]) -> str:
    """한글 글자만 추출 (공백 제거)."""
    return normalize_person_name(text)


def _crop_name_region(thumb_bgr: np.ndarray, band_ratio: float = 0.30) -> np.ndarray:
    """썸네일 하단 band_ratio 비율 영역을 이름 영역으로 크롭."""
    h, w = thumb_bgr.shape[:2]
    band_h = max(20, int(h * band_ratio))
    return thumb_bgr[h - band_h:h, 0:w].copy()


class NameOCR:
    """
    EasyOCR 기반 수강생 이름 추출기.

    OCR 로직을 바꾸려면 이 모듈만 수정하면 됩니다.

    Args:
        lang: EasyOCR 언어 목록 (기본: 한국어+영어)
        gpu: GPU 사용 여부
        teacher_names: 강사 이름 목록 (이 이름은 감지에서 제외)
        band_ratio: 이름 영역 비율 (하단 기준)
    """

    def __init__(
        self,
        lang: list[str] = None,
        gpu: bool = False,
        teacher_names: list[str] = None,
        band_ratio: float = 0.30,
    ):
        import easyocr
        self._reader = easyocr.Reader(lang or ["ko", "en"], gpu=gpu, verbose=False)
        self._teacher_names = resolve_teacher_names(teacher_names)
        self._band_ratio = band_ratio

    def read_name(self, thumb_bgr: np.ndarray) -> tuple[str, float]:
        """
        썸네일에서 이름을 OCR로 읽습니다.

        두 가지 이미지(원본 업스케일, Otsu 이진화)로 읽어 다수결.

        Returns:
            (name, confidence)  name은 한글만, confidence는 0~1
        """
        name_crop = _crop_name_region(thumb_bgr, self._band_ratio)
        if name_crop is None or name_crop.size == 0:
            return "", 0.0

        up = cv2.resize(name_crop, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(up, cv2.COLOR_BGR2GRAY)
        _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        merged: list[str] = []
        for variant in [up, th]:
            try:
                res = self._reader.readtext(variant, detail=0, paragraph=False)
                for t in res:
                    n = _normalize_name(t)
                    if len(n) >= 2:
                        merged.append(n)
            except Exception:
                pass

        if not merged:
            return "", 0.0

        counts = Counter(merged)
        best, votes = counts.most_common(1)[0]
        return best, float(votes / len(merged))

    def is_teacher(self, name: str) -> bool:
        """이름이 강사 목록에 포함되는지 확인."""
        return is_teacher_name(name, self._teacher_names)

    def normalize(self, text: str) -> str:
        """한글만 추출하는 정규화 (외부 사용용)."""
        return _normalize_name(text)
