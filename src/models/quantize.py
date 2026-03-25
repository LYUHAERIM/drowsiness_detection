"""
YOLO 모델 양자화 모듈

- quantize()      : PyTorch native INT8/FP16 양자화 (.pt 저장) — 속도 개선 제한적
- quantize_onnx() : ONNX export + ONNX Runtime INT8 양자화 (.onnx 저장) — 실질적 속도 개선

CLI:
    uv run python src/models/quantize.py --pt checkpoint/yolo11n/weights/best.pt --type int8
    uv run python src/models/quantize.py --pt checkpoint/yolo11n/weights/best.pt --onnx

Jupyter:
    from src.models.quantize import quantize, quantize_onnx

    # PyTorch native (Conv2d 미지원으로 효과 제한)
    out = quantize("checkpoint/yolo11n/weights/best.pt", quant_type="int8")

    # ONNX INT8 (실질적 경량화)
    out = quantize_onnx("checkpoint/yolo11n/weights/best.pt", output_dir="outputs")

    # run_inference와 연동
    summary = run_inference(..., use_onnx=True, onnx_path=out)
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Literal

import torch
import torch.nn as nn

QuantizeType = Literal["int8", "fp16"]

DEFAULT_PT = Path("checkpoint/yolo11n/weights/best.pt")
DEFAULT_OUTPUT_DIR = Path("outputs")
DEFAULT_IMGSZ = 960


def quantize(
    pt_path: str | Path = DEFAULT_PT,
    quant_type: QuantizeType = "int8",
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
) -> Path:
    """YOLO .pt 모델을 PyTorch 네이티브 양자화 후 저장한다.

    Args:
        pt_path:    원본 YOLO .pt 모델 경로
        quant_type: "int8" (dynamic) | "fp16"
        output_dir: 저장 디렉토리 (default: outputs/)

    Returns:
        저장된 양자화 모델 경로 (.pt)
    """
    from ultralytics import YOLO

    pt_path = Path(pt_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not pt_path.exists():
        raise FileNotFoundError(f".pt 모델을 찾을 수 없습니다: {pt_path}")

    print(f"[quantize] 모델:  {pt_path}")
    print(f"[quantize] 방식:  {quant_type}")

    t0 = time.perf_counter()

    torch_model = YOLO(str(pt_path)).model
    torch_model.eval()

    if quant_type == "int8":
        quantized = torch.quantization.quantize_dynamic(
            torch_model,
            {nn.Linear, nn.Conv2d},
            dtype=torch.qint8,
        )
    elif quant_type == "fp16":
        quantized = torch_model.half()
    else:
        raise ValueError(f"지원하지 않는 양자화 타입: {quant_type}")

    dest = output_dir / f"{pt_path.stem}_{quant_type}.pt"
    torch.save(quantized, dest)

    elapsed = time.perf_counter() - t0
    orig_mb = pt_path.stat().st_size / 1024 / 1024
    dest_mb = dest.stat().st_size / 1024 / 1024
    print(f"[quantize] 완료:  {elapsed:.1f}s")
    print(f"[quantize] 크기:  {orig_mb:.1f} MB → {dest_mb:.1f} MB")
    print(f"[quantize] 저장:  {dest}")

    return dest


def quantize_onnx(
    pt_path: str | Path = DEFAULT_PT,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    imgsz: int = DEFAULT_IMGSZ,
) -> Path:
    """YOLO .pt → FP32 ONNX export → ONNX Runtime INT8 동적 양자화.

    Args:
        pt_path:    원본 YOLO .pt 모델 경로
        output_dir: 저장 디렉토리 (default: outputs/)
        imgsz:      모델 입력 해상도 (default: 960)

    Returns:
        저장된 INT8 ONNX 모델 경로
    """
    from onnxruntime.quantization import QuantType, quantize_dynamic
    from ultralytics import YOLO

    pt_path = Path(pt_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not pt_path.exists():
        raise FileNotFoundError(f".pt 모델을 찾을 수 없습니다: {pt_path}")

    print(f"[quantize_onnx] 모델:  {pt_path}")
    t0 = time.perf_counter()

    # Step 1: FP32 ONNX export
    print("[quantize_onnx] Step 1: ONNX export...")
    model = YOLO(str(pt_path))
    exported = Path(model.export(format="onnx", imgsz=imgsz))

    # Step 2: ONNX Runtime INT8 동적 양자화
    print("[quantize_onnx] Step 2: INT8 양자화...")
    dest = output_dir / f"{pt_path.stem}_int8.onnx"
    quantize_dynamic(str(exported), str(dest), weight_type=QuantType.QInt8)
    exported.unlink()  # 중간 FP32 ONNX 제거

    elapsed = time.perf_counter() - t0
    orig_mb = pt_path.stat().st_size / 1024 / 1024
    dest_mb = dest.stat().st_size / 1024 / 1024
    print(f"[quantize_onnx] 완료:  {elapsed:.1f}s")
    print(f"[quantize_onnx] 크기:  {orig_mb:.1f} MB (.pt) → {dest_mb:.1f} MB (.onnx int8)")
    print(f"[quantize_onnx] 저장:  {dest}")

    return dest


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="YOLO .pt 모델 양자화",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--pt", type=Path, default=DEFAULT_PT, help="원본 YOLO .pt 경로")
    parser.add_argument(
        "--type", dest="quant_type", choices=["int8", "fp16"], default="int8", help="PyTorch native 양자화 방식"
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="저장 디렉토리")
    parser.add_argument("--imgsz", type=int, default=DEFAULT_IMGSZ, help="모델 입력 해상도")
    parser.add_argument("--onnx", action="store_true", help="ONNX Runtime INT8 양자화 사용 (권장)")
    args = parser.parse_args()

    if args.onnx:
        result = quantize_onnx(pt_path=args.pt, output_dir=args.output_dir, imgsz=args.imgsz)
    else:
        result = quantize(pt_path=args.pt, quant_type=args.quant_type, output_dir=args.output_dir)
    print(f"\n저장 완료: {result}")
