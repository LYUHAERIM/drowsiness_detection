import os
import re
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

import cv2
import numpy as np


@dataclass
class VideoInfo:
    video_id: str
    date: str
    start_time: Optional[datetime]
    frame_dir: Path
    frame_count: int
    label: str  # "normal" or "escape"


@dataclass
class DatasetSummary:
    normal_videos: list = field(default_factory=list)
    escape_videos: list = field(default_factory=list)

    @property
    def total_normal_frames(self):
        return sum(v.frame_count for v in self.normal_videos)

    @property
    def total_escape_frames(self):
        return sum(v.frame_count for v in self.escape_videos)

    @property
    def total_frames(self):
        return self.total_normal_frames + self.total_escape_frames

    @property
    def all_videos(self):
        return self.normal_videos + self.escape_videos


def _count_frames(directory: Path) -> int:
    return len(list(directory.glob("frame_*.jpg")))


def _parse_video_meta(folder_name: str):
    """kdt-backendj-19th_XXXXX_YYYY-MM-DD-HH-MM-SS 형식에서 id, date, start_time 파싱"""
    pattern = r"kdt-backendj-19th_(\w+)_(\d{4}-\d{2}-\d{2})-(\d{2})-(\d{2})-(\d{2})"
    match = re.search(pattern, folder_name)
    if match:
        video_id = match.group(1)
        date     = match.group(2)
        start_time = datetime.strptime(
            f"{date} {match.group(3)}:{match.group(4)}:{match.group(5)}",
            "%Y-%m-%d %H:%M:%S"
        )
        return video_id, date, start_time
    return folder_name, "unknown", None


def load_dataset(conversion_root: Path) -> DatasetSummary:
    """
    conversion 폴더 구조를 읽어 DatasetSummary를 반환합니다.

    Args:
        conversion_root: data/conversion 경로

    Returns:
        DatasetSummary 객체
    """
    summary = DatasetSummary()

    # 수강생 녹화 영상 (정상 레이블)
    normal_dir = conversion_root / "수강생 녹화 영상"
    if normal_dir.exists():
        for folder in sorted(normal_dir.iterdir()):
            if not folder.is_dir():
                continue
            video_id, date, start_time = _parse_video_meta(folder.name)
            count = _count_frames(folder)
            summary.normal_videos.append(VideoInfo(
                video_id=video_id,
                date=date,
                start_time=start_time,
                frame_dir=folder,
                frame_count=count,
                label="normal",
            ))

    # 이탈 영상
    escape_dir = conversion_root / "이탈 영상"
    if escape_dir.exists():
        count = _count_frames(escape_dir)
        # 폴더 자체가 하나의 영상
        files = list(escape_dir.glob("frame_*.jpg"))
        if files:
            summary.escape_videos.append(VideoInfo(
                video_id="z6q0fy",
                date="2025-10-13",
                start_time=datetime(2025, 10, 13, 8, 47, 32),
                frame_dir=escape_dir,
                frame_count=count,
                label="escape",
            ))

    return summary


def load_frames(frame_dir: Path, max_frames: int = None, step: int = 1) -> list[np.ndarray]:
    """
    지정된 폴더에서 프레임을 로드합니다.

    Args:
        frame_dir: frame_N.jpg 파일이 있는 폴더
        max_frames: 최대 로드 프레임 수 (None이면 전체)
        step: 몇 프레임마다 샘플링 (default=1, 전체)

    Returns:
        numpy 배열 리스트 [(H, W, C), ...]
    """
    frame_files = sorted(
        frame_dir.glob("frame_*.jpg"),
        key=lambda p: int(re.search(r"(\d+)", p.stem).group(1))
    )

    if step > 1:
        frame_files = frame_files[::step]
    if max_frames:
        frame_files = frame_files[:max_frames]

    frames = []
    for fp in frame_files:
        img = cv2.imread(str(fp))
        if img is not None:
            frames.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return frames


def sample_frames(frame_dir: Path, n: int = 9, seed: int = 42) -> list[np.ndarray]:
    """
    폴더에서 n개 프레임을 랜덤 샘플링합니다. (시각화용)

    Args:
        frame_dir: 프레임 폴더
        n: 샘플 수
        seed: 랜덤 시드

    Returns:
        numpy 배열 리스트
    """
    frame_files = list(frame_dir.glob("frame_*.jpg"))
    rng = np.random.default_rng(seed)
    sampled = rng.choice(frame_files, size=min(n, len(frame_files)), replace=False)
    frames = []
    for fp in sorted(sampled):
        img = cv2.imread(str(fp))
        if img is not None:
            frames.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return frames


def get_frame_shape(frame_dir: Path) -> tuple[int, int, int]:
    """
    폴더 내 첫 번째 프레임의 shape를 반환합니다.

    Returns:
        (height, width, channels)
    """
    first = next(iter(sorted(frame_dir.glob("frame_*.jpg"))), None)
    if first is None:
        return (0, 0, 0)
    img = cv2.imread(str(first))
    return img.shape if img is not None else (0, 0, 0)
