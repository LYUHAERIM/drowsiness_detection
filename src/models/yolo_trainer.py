from pathlib import Path
from typing import Literal

import numpy as np
from ultralytics import YOLO

VARIANTS = Literal["n", "s", "m"]
CLASS_NAMES = {0: "person_on", 1: "person_off", 2: "screen_off"}


def load_model(variant: VARIANTS = "n") -> YOLO:
    """
    YOLO11 모델을 로드합니다. (pretrained weights 자동 다운로드)

    Args:
        variant: 모델 크기 "n" | "s" | "m"

    Returns:
        YOLO 모델 객체
    """
    model_name = f"yolo11{variant}.pt"
    return YOLO(model_name)


def train_model(
    model: YOLO,
    data_yaml: str | Path,
    epochs: int = 100,
    imgsz: int = 640,
    batch: int = 16,
    lr0: float = 0.01,
    lrf: float = 0.01,
    momentum: float = 0.937,
    weight_decay: float = 0.0005,
    warmup_epochs: float = 3.0,
    dropout: float = 0.0,
    patience: int = 20,
    workers: int = 4,
    project: str = "checkpoints",
    name: str | None = None,
    plots: bool = False,
) -> None:
    """
    YOLO11 모델을 학습합니다.

    Args:
        model: load_model()로 로드한 YOLO 객체
        data_yaml: data.yaml 경로
        epochs: 학습 에폭 수
        imgsz: 입력 이미지 크기
        batch: 배치 사이즈 (T4: 16, L4: 32, A100: 64)
        lr0: 초기 학습률
        lrf: 최종 학습률 비율 (lr0 * lrf)
        momentum: SGD momentum / Adam beta1
        weight_decay: L2 규제 (과적합 방지)
        warmup_epochs: 학습률 워밍업 에폭 수
        dropout: dropout 비율 (0.0이면 비활성화)
        patience: early stopping 기준 에폭 수 (0이면 비활성화)
        workers: 데이터 로더 병렬 워커 수 (T4: 2, L4: 4, A100: 8)
        project: 결과 저장 루트 경로
        name: 실험 이름 (None이면 자동 생성)
        plots: confusion matrix, val batch 예측 이미지 등 저장 여부
    """
    model.train(
        data=str(data_yaml),
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        lr0=lr0,
        lrf=lrf,
        momentum=momentum,
        weight_decay=weight_decay,
        warmup_epochs=warmup_epochs,
        dropout=dropout,
        patience=patience,
        workers=workers,
        project=project,
        name=name,
        plots=plots,
    )


def evaluate_model(
    model: YOLO,
    data_yaml: str | Path,
    imgsz: int = 640,
) -> dict:
    """
    학습된 모델을 val set으로 평가합니다.

    Args:
        model: 학습된 YOLO 객체
        data_yaml: data.yaml 경로
        imgsz: 입력 이미지 크기

    Returns:
        metrics dict (mAP50, mAP50-95 등)
    """
    metrics = model.val(data=str(data_yaml), imgsz=imgsz)
    return metrics


def predict(
    model: YOLO,
    source: str | Path | np.ndarray,
    imgsz: int = 640,
    conf: float = 0.5,
) -> list[dict]:
    """
    단일 이미지 또는 프레임에서 객체를 검출합니다.
    파이프라인 다음 단계(OCR, MediaPipe)로 전달할 결과를 반환합니다.

    Args:
        model: 학습된 YOLO 객체
        source: 이미지 경로 또는 BGR numpy 배열
        imgsz: 입력 이미지 크기
        conf: confidence threshold

    Returns:
        검출 결과 리스트. 각 항목:
            {
                "class_id": int,
                "class_name": str,
                "confidence": float,
                "bbox": [x1, y1, x2, y2],  # 픽셀 좌표
            }
    """
    results = model.predict(source=source, imgsz=imgsz, conf=conf, verbose=False)
    detections = []
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls.item())
            detections.append({
                "class_id": cls_id,
                "class_name": CLASS_NAMES.get(cls_id, str(cls_id)),
                "confidence": round(float(box.conf.item()), 4),
                "bbox": [round(v, 2) for v in box.xyxy[0].tolist()],
            })
    return detections
