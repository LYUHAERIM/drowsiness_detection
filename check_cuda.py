import platform
import sys

import torch

from app.inference.device import get_runtime_diagnostics


def main():
    print("[SMOKE TEST] Drowsiness Detection Device Smoke Test")
    print("Python", sys.version.replace("\n", " "))
    print("Platform:", platform.platform())
    print("torch", torch.__version__)

    for line in get_runtime_diagnostics():
        print(line)

    if torch.cuda.is_available():
        try:
            props = torch.cuda.get_device_properties(0)
            print("Primary CUDA capability:", f"{props.major}.{props.minor}")
            print("Primary CUDA total memory (GB):", round(props.total_memory / (1024 ** 3), 2))
        except Exception as exc:
            print("CUDA property read failed:", exc)
    else:
        print("CUDA 미사용 상태입니다. NVIDIA 드라이버 / CUDA 지원 PyTorch 설치 / GPU 인식 여부를 확인하세요.")


if __name__ == "__main__":
    main()
