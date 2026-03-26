import platform
from typing import Optional

import torch


def select_device(prefer_mps: bool = True) -> str:
    """Select the best available runtime device with safe fallback."""
    try:
        if torch.cuda.is_available():
            return "cuda:0"
    except Exception:
        pass

    if prefer_mps:
        try:
            mps = getattr(getattr(torch, "backends", None), "mps", None)
            if mps is not None and mps.is_available():
                return "mps"
        except Exception:
            pass

    return "cpu"


def is_gpu_device(device: str | int | None) -> bool:
    if isinstance(device, str):
        return device.startswith("cuda") or device == "mps"
    if isinstance(device, int):
        return device >= 0
    return False


def get_device_name(device: Optional[str] = None) -> str:
    resolved = device or select_device()
    if resolved.startswith("cuda"):
        try:
            index = int(resolved.split(":", 1)[1]) if ":" in resolved else 0
            return torch.cuda.get_device_name(index)
        except Exception:
            return "NVIDIA GPU"
    if resolved == "mps":
        return "Apple Metal"
    return "CPU"


def get_device_summary(device: Optional[str] = None) -> str:
    resolved = device or select_device()
    if resolved.startswith("cuda"):
        return f"{resolved} ({get_device_name(resolved)})"
    return resolved


def get_runtime_diagnostics() -> list[str]:
    lines = [
        f"Platform: {platform.platform()}",
        f"Python: {platform.python_version()}",
        f"PyTorch: {torch.__version__}",
    ]

    try:
        cuda_available = torch.cuda.is_available()
    except Exception as exc:
        cuda_available = False
        lines.append(f"CUDA check failed: {exc}")
    else:
        lines.append(f"CUDA available: {cuda_available}")

    if cuda_available:
        try:
            count = torch.cuda.device_count()
            lines.append(f"CUDA device count: {count}")
            for index in range(count):
                lines.append(f"cuda:{index}: {torch.cuda.get_device_name(index)}")
        except Exception as exc:
            lines.append(f"CUDA device query failed: {exc}")

    mps_available = False
    try:
        mps = getattr(getattr(torch, "backends", None), "mps", None)
        mps_available = mps is not None and mps.is_available()
    except Exception as exc:
        lines.append(f"MPS check failed: {exc}")
    else:
        lines.append(f"MPS available: {mps_available}")

    selected = select_device(prefer_mps=True)
    lines.append(f"Selected device: {selected}")
    lines.append(f"Selected device name: {get_device_name(selected)}")
    return lines
