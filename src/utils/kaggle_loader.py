import shutil
import kagglehub
from pathlib import Path


def download_kaggle_dataset(
    dataset_handle: str,
    save_dir: Path | str | None = None,
    force: bool = False,
) -> Path:
    """
    Kaggle 데이터셋을 다운로드합니다.

    Args:
        dataset_handle: Kaggle 데이터셋 식별자 (예: "akashshingha850/mrl-eye-dataset")
        save_dir: 다운로드 후 복사할 경로 (None이면 kagglehub 기본 캐시 경로 사용)
        force: True면 이미 save_dir에 존재해도 재다운로드

    Returns:
        최종 데이터셋 경로 (Path)

    Examples:
        >>> path = download_kaggle_dataset(
        ...     "akashshingha850/mrl-eye-dataset",
        ...     save_dir=PROJECT_ROOT / "data/external/mrl-eye-dataset",
        ... )
    """
    if save_dir is not None:
        save_dir = Path(save_dir)
        if save_dir.exists() and not force:
            print(f"[kaggle] 이미 존재합니다: {save_dir}")
            return save_dir

    print(f"[kaggle] 다운로드 중: {dataset_handle}")
    cached_path = Path(kagglehub.dataset_download(dataset_handle))
    print(f"[kaggle] 캐시 경로: {cached_path}")

    if save_dir is not None:
        save_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(cached_path, save_dir, dirs_exist_ok=True)
        print(f"[kaggle] 저장 완료: {save_dir}")
        return save_dir

    return cached_path
