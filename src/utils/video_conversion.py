import math
import os
from pathlib import Path
from typing import Iterator, Optional

import cv2
import numpy as np


# ─────────────────────────────────────────────────────────────────────────────
# VideoReader / VideoWriter  (파이프라인용 컨텍스트 매니저)
# ─────────────────────────────────────────────────────────────────────────────

class VideoReader:
    """
    영상 파일을 프레임 단위로 순회하는 컨텍스트 매니저.

    target_fps를 설정하면 원본 FPS 기준 stride로 서브샘플링합니다.

    Args:
        path:       영상 파일 경로
        start_sec:  시작 지점 (초)
        end_sec:    종료 지점 (초, None이면 끝까지)
        target_fps: 목표 FPS (None이면 원본 FPS 전체 사용)

    Example::

        with VideoReader("video.mp4", target_fps=10) as reader:
            for frame_idx, ts, frame in reader:
                ...
    """

    def __init__(
        self,
        path,
        start_sec: float = 0.0,
        end_sec: Optional[float] = None,
        target_fps: Optional[float] = None,
    ):
        self._path = str(path)
        self._start_sec = start_sec
        self._end_sec = end_sec
        self._target_fps = target_fps
        self._cap: Optional[cv2.VideoCapture] = None

    # ── 프로퍼티 ──────────────────────────────────────────────────────────────

    @property
    def fps(self) -> float:
        """원본 영상 FPS."""
        return self._cap.get(cv2.CAP_PROP_FPS) if self._cap else 0.0

    @property
    def fps_effective(self) -> float:
        """실제 출력 FPS (target_fps 또는 원본 FPS)."""
        return self._target_fps if self._target_fps else self.fps

    @property
    def width(self) -> int:
        return int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)) if self._cap else 0

    @property
    def height(self) -> int:
        return int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) if self._cap else 0

    @property
    def total_frames(self) -> int:
        return int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT)) if self._cap else 0

    # ── 컨텍스트 매니저 ───────────────────────────────────────────────────────

    def open(self) -> "VideoReader":
        self._cap = cv2.VideoCapture(self._path)
        if not self._cap.isOpened():
            raise IOError(f"영상을 열 수 없습니다: {self._path}")
        fps = self.fps
        start_frame = max(0, int(self._start_sec * fps))
        self._cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        self._start_frame = start_frame
        self._end_frame = (
            min(self.total_frames, int(self._end_sec * fps))
            if self._end_sec is not None else self.total_frames
        )
        self._stride = max(1, int(round(fps / self._target_fps))) if self._target_fps else 1
        return self

    def close(self):
        if self._cap:
            self._cap.release()
            self._cap = None

    def __enter__(self) -> "VideoReader":
        return self.open()

    def __exit__(self, *_):
        self.close()

    # ── 순회 ─────────────────────────────────────────────────────────────────

    def __iter__(self) -> Iterator[tuple[int, float, np.ndarray]]:
        """
        Yields:
            (frame_idx, timestamp_sec, frame_bgr)
        """
        if self._cap is None:
            raise RuntimeError("VideoReader가 열려있지 않습니다. with 문 또는 open()을 먼저 호출하세요.")

        fps = self.fps
        frame_idx = self._start_frame

        while frame_idx < self._end_frame:
            ret, frame = self._cap.read()
            if not ret:
                break
            if (frame_idx - self._start_frame) % self._stride == 0:
                ts = frame_idx / max(fps, 1e-6)
                yield frame_idx, ts, frame
            frame_idx += 1

    def __len__(self) -> int:
        """예상 출력 프레임 수."""
        return math.ceil((self._end_frame - self._start_frame) / self._stride)


class VideoWriter:
    """
    영상 파일 저장 컨텍스트 매니저.

    Args:
        path:    출력 파일 경로
        fps:     저장 FPS
        width:   프레임 너비
        height:  프레임 높이

    Example::

        with VideoWriter("output.mp4", fps=10, width=1620, height=720) as writer:
            writer.write(canvas)
    """

    def __init__(self, path, fps: float, width: int, height: int):
        self._path = str(path)
        self._fps = fps
        self._width = width
        self._height = height
        self._writer: Optional[cv2.VideoWriter] = None

    def open(self) -> "VideoWriter":
        Path(self._path).parent.mkdir(parents=True, exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self._writer = cv2.VideoWriter(self._path, fourcc, self._fps, (self._width, self._height))
        if not self._writer.isOpened():
            raise IOError(f"VideoWriter를 열 수 없습니다: {self._path}")
        return self

    def write(self, frame: np.ndarray) -> None:
        """프레임을 저장합니다."""
        if self._writer:
            self._writer.write(frame)

    def release(self):
        if self._writer:
            self._writer.release()
            self._writer = None

    def __enter__(self) -> "VideoWriter":
        return self.open()

    def __exit__(self, *_):
        self.release()


# ─────────────────────────────────────────────────────────────────────────────
# 기존 유틸 함수 (프레임 추출)
# ─────────────────────────────────────────────────────────────────────────────

def extract_frames_video(video_path, output_dir, interval_sec=1, prefix=None):
    """
    영상(mp4)에서 일정 간격으로 프레임을 추출하는 함수

    Args:
        video_path (str): 영상 파일 경로
        output_dir (str): 프레임 저장 폴더
        interval_sec (int): 몇 초마다 프레임 추출할지 (default=1초)
        prefix (str): 저장 파일명 접두사 (default: None → 영상 파일명 사용)
    """

    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))

    if prefix is None:
        prefix = os.path.splitext(os.path.basename(video_path))[0]

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_sec)

    frame_id = 0
    saved_id = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % frame_interval == 0:
            save_path = os.path.join(output_dir, f"{prefix}_frame_{saved_id}.jpg")
            cv2.imwrite(save_path, frame)
            saved_id += 1

        frame_id += 1

    cap.release()
    print(f"총 {saved_id}개의 프레임 저장")


def extract_frames_from_folder(input_dir, output_root, interval_sec=1):
    """
    폴더 내 모든 mp4 영상을 순회하며 프레임을 추출하는 함수

    Args:
        input_dir (str or Path): 영상이 들어있는 폴더
        output_root (str or Path): 프레임을 저장할 루트 폴더
        interval_sec (float): 몇 초마다 프레임을 추출할지
    """

    for file_name in os.listdir(input_dir):
        if not file_name.lower().endswith(".mp4"):
            continue

        video_path = os.path.join(input_dir, file_name)
        video_name = os.path.splitext(file_name)[0]
        output_dir = os.path.join(output_root, video_name)

        print(f"Processing: {file_name}")
        extract_frames_video(video_path, output_dir, interval_sec)