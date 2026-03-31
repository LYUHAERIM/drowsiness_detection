<div align="center">

<h1>실시간 수강생 졸음 감지 시스템</h1>

<p>
  <strong>Zoom 화면 기반 수강생 졸음·이탈 자동 감지 AI 시스템</strong><br>
  End-to-end pipeline: Zoom 화면 → YOLO 탐지 → OCR 이름 인식 → FaceMesh 분석 → 룰 기반 졸음 판별 → Gradio 대시보드
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/YOLO11n-mAP50%200.993-EE4C2C?style=flat-square&logo=ultralytics&logoColor=white">
  <img src="https://img.shields.io/badge/MediaPipe-FaceMesh-00BCD4?style=flat-square&logo=google&logoColor=white">
  <img src="https://img.shields.io/badge/EasyOCR-이름인식-4CAF50?style=flat-square">
  <img src="https://img.shields.io/badge/Gradio-대시보드-FF7C00?style=flat-square&logo=gradio&logoColor=white">
  <img src="https://img.shields.io/badge/uv-패키지관리-6E40C9?style=flat-square">
</p>

**📌 데모 영상 추가 예정**

<!-- https://github.com/user-attachments/assets/여기에-영상-URL -->

</div>

---

## Team

<br>

<div align="center">

| <img src="https://github.com/GH-Door.png" width="100"> | <img src="https://github.com/adhoc0909.png" width="100"> | <img src="https://github.com/LYUHAERIM.png" width="100"> |
|:---:|:---:|:---:|
| [GH-Door](https://github.com/GH-Door) | [adhoc0909](https://github.com/adhoc0909) | [LYUHAERIM](https://github.com/LYUHAERIM) |
| 문국현 | 이호욱 | 류혜림 |

</div>

<br>

---

## Overview

| 항목 | 내용 |
|:-----|:-----|
| **📅 Date** | 2026.03 ~ 2026.04 |
| **👥 Type** | 팀 프로젝트 (3인 1팀) |
| **🎯 Goal** | 웹캠·Zoom 화면 기반 실시간 수강생 졸음·이탈 자동 감지 시스템 구축 |
| **🔧 Tech Stack** | Python 3.12, YOLO11n, MediaPipe, EasyOCR, Gradio, OpenCV, PyTorch |
| **📊 Dataset** | 자체 수집 Zoom 화면 영상 (1,500장 직접 라벨링, 3 클래스) |

<br>

Zoom 화면 공유 영상 기반 수강생 졸음·이탈 자동 감지 AI 파이프라인.  
논문 기반 파라미터 설계 + 3계층 룰 기반 상태 머신 + 다층 오탐 방지 전략 적용.

**핵심 특징:**
- **YOLO11n** 커스텀 학습 — 자체 수집·라벨링 1,500장, mAP50 = **0.993**, 4에폭 수렴
- **3계층 졸음 판별** — Level1(FaceMesh EAR+보조) → Level2(얼굴 위치 fallback) → Level3(모션 hold)
- **EasyOCR 이름 인식** — 슬롯 하단 이름 자동 추출, 다수결 투표로 안정화
- **논문/가이드라인 8건** 참조, 파라미터 30개+ 학술 근거 기반 설계
- **실시간 Gradio 대시보드** — 웹캠/영상 업로드 모두 지원

---

## 📊 Results

YOLO11n 커스텀 모델 최종 학습 결과 — 자체 수집 Zoom 화면 데이터셋 (3 클래스, 4 epochs)

| Precision | Recall | mAP50 | mAP50-95 |
|:---------:|:------:|:-----:|:--------:|
| 0.996 | 0.998 | **0.993** | 0.931 |

**실시간 추론 성능 (Apple M 시리즈 MPS 기준):**
- 평균 처리 속도: ~30.1ms / 프레임
- FaceMesh 병렬 처리: ThreadPoolExecutor (최대 5 workers)
- CLAHE 저조도 전처리 포함 기준

---

## 🏗️ System Architecture

<div align="center">

**📌 파이프라인 도식 이미지 추가 예정**

<!-- <img src="assets/pipeline.png" width="90%"> -->

</div>

**파이프라인 흐름:** `웹캠/영상` → `YOLO11n 탐지` → `슬롯 매칭 (Hungarian)` → `EasyOCR 이름 인식` → `FaceMesh (EAR/MAR/pitch)` → `3계층 졸음 판별` → `Gradio 대시보드 / CSV 저장`

**감지 상태:** `NORMAL` | `DROWSY` | `YAWN` | `ABSENT` | `IGNORE` | `NOT FOUND` _(noface 시 시각화 전용 표시)_

---

## 🔎 Drowsiness Detection Algorithm

### 3계층 룰 기반 상태 머신

| 계층 | 조건 | 설명 |
|:-----|:-----|:-----|
| **Level 1** | EAR < baseline × 0.75 (또는 < 0.20) + 보조 신호 1개 이상 | FaceMesh 랜드마크 기반 복합 조건 |
| **Level 2** | face_center_y 급락 + PoseDetector fallback | FaceMesh 실패 시 얼굴 위치·Pose로 감지 |
| **Level 3** | 모션 없음 지속 (노face hold) | 얼굴 미감지 상태에서 모션 홀드 |

**보조 신호:** MAR > 0.50 (하품), pitch_like 급증 (고개 끄덕임), tilt_deg > 15° (고개 기울임), PERCLOS ≥ 0.15 (30초 윈도우 눈 감김 비율)

### 논문 기반 파라미터 설계

| 파라미터 | 값 | 근거 |
|:---------|:---|:-----|
| EAR 절대 임계값 | 0.20 | Soukupová & Čech 2016 |
| EAR hold 시간 | 1.0초 | Soukupová & Čech 2016 |
| PERCLOS 윈도우 | 30초 | NHTSA (미국 도로교통안전국) |
| PERCLOS 임계값 | 0.15 | ARVO Journal |
| MAR 임계값 | 0.50 | LearnOpenCV + IRJMETS 2024 |
| 하품 최소 지속 | 2초 | PMC 2024 |
| 고개 끄덕임 hold | 1.5초 | Springer 2021 |
| 기울기 임계값 | 15° | Multi-feature Fuzzy Inference |

### 오탐 방지 다층 방어 전략

| 전략 | 내용 |
|:-----|:-----|
| 복합 조건 필수 | EAR 단독 DROWSY 불가 — 보조 신호 1개 이상 필수, 깜빡임 오탐 원천 차단 |
| 하품-PERCLOS 충돌 해결 | 하품 중 눈 찡그림 → PERCLOS·ear_low_frames 누적에서 자동 제외 |
| 눈뜸 게이트 | 현재 EAR ≥ threshold × 1.2 이면 과거 PERCLOS 누적에도 DROWSY 차단 |
| EMA baseline 오염 방지 | EAR < 0.10 또는 > 0.45 프레임은 개인 기준선 갱신 제외 |
| Wakeup 감지 | 모션 > 20.0 이 0.5초 지속 시 PERCLOS·타이머 즉시 전체 리셋 |

---

## 🛠️ Installation

### 요구 사항

- Python ≥ 3.12
- macOS (MPS) / Linux (CUDA) / Windows (CPU) 지원
- 웹캠 또는 Zoom 화면 공유 영상 (mp4)

### 1. 의존성 설치

```bash
# uv 설치 (없는 경우)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 의존성 동기화
uv sync
```

### 2. 체크포인트 확인

```
checkpoint/
└── yolo11n/
    └── weights/
        └── best.pt   ← 기본 사용 모델 (mAP50 0.993)
```

---

## 🚀 Quick Start

### 영상 추론 (CLI)

```bash
uv run python scripts/infer_video.py \
  --input data/video/TestVideo2.mp4 \
  --checkpoint checkpoint/yolo11n/weights/best.pt \
  --output outputs/result.mp4 \
  --fps 10.0
```

### Gradio 대시보드 실행

```bash
uv run python gradio_app.py
```

`http://localhost:7860` 접속 — 웹캠 실시간 감지 및 영상 업로드 추론 지원

### JupyterLab

```bash
uv run jupyter lab
```

---

## ⚙️ Configuration

`scripts/infer_video.py`의 `PipelineConfig`에서 주요 설정 변경 가능:

```python
config = PipelineConfig(
    target_fps=10.0,              # 처리 FPS (원본보다 낮게 설정 시 서브샘플링)
    start_sec=0, end_sec=120,     # 처리 구간 (초)
    teacher_names=["강경미"],     # 강사 이름 → IGNORE 처리
    yolo_conf=0.10,               # YOLO 탐지 신뢰도 임계값
    drowsiness=DrowsinessConfig(
        ear_ratio=0.75,           # 기준선 대비 EAR 감소 비율 (기본값)
        ear_hold_strong_sec=0.5,  # EAR + 보조 → DROWSY 진입 시간
        ear_hold_weak_sec=1.5,    # EAR 단독 → DROWSY 진입 시간
        tilt_deg_thresh=15.0,     # 고개 기울기 임계값 (도)
        mar_init_abs=0.50,        # MAR 절대 임계값
    ),
)
```

---

## 📁 Project Structure

```
drowsiness_detection/
├── scripts/
│   └── infer_video.py        # 진입점. PipelineConfig, ZoomPipeline, run_inference()
├── src/
│   ├── detection/
│   │   ├── drowsiness.py     # 졸음 판별 상태 머신 (3계층 룰 기반, DrowsinessConfig)
│   │   ├── face.py           # MediaPipe FaceMesh (EAR/MAR/pitch/tilt, CLAHE)
│   │   ├── pose.py           # Pose fallback (FaceMesh 실패 시 고개 숙임 감지)
│   │   └── metrics.py        # EAR/MAR 계산 유틸리티
│   ├── tracking/
│   │   └── slot.py           # 슬롯 트래킹 (SlotState, Hungarian 매칭, bbox 안정화)
│   ├── ocr/
│   │   └── reader.py         # EasyOCR 이름 추출 (NameOCR, 다수결 투표)
│   ├── visual/
│   │   └── annotator.py      # 화면 오버레이 (bbox, info box, 상태 색상)
│   ├── utils/
│   │   └── video_conversion.py  # VideoReader / VideoWriter (FPS stride 지원)
│   └── models/
│       └── yolo_trainer.py   # YOLO 학습 유틸리티
├── app/
│   ├── inference/
│   │   └── live_engine.py    # LiveZoomEngine (Gradio 실시간 추론 엔진)
│   └── ui/                   # Gradio UI 컴포넌트
├── checkpoint/
│   └── yolo11n/weights/best.pt   # 학습된 YOLO11n 가중치
├── jupyter/                  # EDA, 파이프라인 실험 노트북
├── outputs/                  # 추론 결과 영상 + CSV
├── gradio_app.py             # Gradio 앱 진입점
└── pyproject.toml
```

---

## 🔧 Modification Guide

| 수정 목표 | 파일 |
|:----------|:-----|
| YOLO 탐지 임계값 | `scripts/infer_video.py` → `PipelineConfig.yolo_conf` |
| 졸음 임계값 (EAR, MAR, pitch 등) | `scripts/infer_video.py` → `DrowsinessConfig` |
| 졸음 판별 알고리즘 | `src/detection/drowsiness.py` → `update_drowsiness_state()` |
| 얼굴 특징 추출 | `src/detection/face.py` → `FaceMeshDetector` |
| 이름 OCR 로직 | `src/ocr/reader.py` → `NameOCR` |
| 강사 이름 목록 | `scripts/infer_video.py` → `PipelineConfig.teacher_names` |
| 슬롯 매칭·bbox 안정화 | `src/tracking/slot.py` |
| 화면 색상·레이아웃 | `src/visual/annotator.py` |
| 영상 FPS·구간 설정 | `scripts/infer_video.py` → `PipelineConfig.target_fps / start_sec / end_sec` |

---

## 🙏 Acknowledgements

**라이브러리**
- [Ultralytics YOLO11](https://github.com/ultralytics/ultralytics) — 객체 탐지 백본
- [MediaPipe](https://github.com/google-ai-edge/mediapipe) — FaceMesh / Pose 랜드마크
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) — 이름 OCR

**참고 논문 및 가이드라인**
- [Soukupová & Čech 2016](https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf) — EAR 절대 임계값 0.20, hold 1.0초
- [NHTSA DOT HS 808 707](https://www.nhtsa.gov/sites/nhtsa.gov/files/808707.pdf) — PERCLOS 30초 윈도우 권장
- [ARVO Journal of Vision](https://jov.arvojournals.org/article.aspx?articleid=2141193) — PERCLOS 임계값 0.15 (실제 주행 최적값)
- [PMC 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11644966/) — 하품 최소 지속 2초 (복합 조건)
- [Springer 2021](https://link.springer.com/chapter/10.1007/978-981-16-5987-4_63) — 고개 끄덕임 hold 1.5초
- [IRJMETS 2024](https://www.irjmets.com/uploadedfiles/paper//issue_4_april_2024/54235/final/fin_irjmets1714307792.pdf) — MAR 임계값 0.50 (MediaPipe 기준)
- [LearnOpenCV](https://learnopencv.com/driver-drowsiness-detection-using-mediapipe-in-python/) — MediaPipe FaceMesh EAR/MAR 구현
- [ScienceDirect — Fuzzy Inference System](https://www.sciencedirect.com/science/article/abs/pii/S0957417407000401) — 고개 기울기 15° 임계값

---

## License

MIT License — 자세한 내용은 [LICENSE](LICENSE) 참조
