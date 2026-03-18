# 졸음 감지 파이프라인 인수인계 문서

## 실행

```bash
uv sync
uv run python scripts/infer_video.py
```

`scripts/infer_video.py` 하단의 경로 변수 수정:

```python
CHECKPOINT   = Path("checkpoint/yolo11n/weights/best.pt")  # YOLO 가중치
VIDEO_PATH   = Path("data/video/TestVideo2.mp4")            # 입력 영상
OUTPUT_VIDEO = Path("data/video/output.mp4")                # 출력 영상
```

---

## 기능별 수정 파일

| 수정하고 싶은 기능 | 파일 |
|---|---|
| YOLO 탐지 임계값 / 클래스 | `scripts/infer_video.py` → `PipelineConfig.yolo_conf` |
| 졸음 판별 임계값 (EAR, MAR, pitch 등) | `scripts/infer_video.py` → `PipelineConfig.drowsiness` |
| 졸음 판별 **알고리즘** (규칙 자체 변경) | `src/detection/drowsiness.py` |
| 얼굴 특징 추출 (EAR 계산, CLAHE, 랜드마크) | `src/detection/face.py` → `FaceMeshDetector` |
| 이름 OCR 로직 | `src/ocr/reader.py` → `NameOCR` |
| 강사 이름 목록 | `scripts/infer_video.py` → `PipelineConfig.teacher_names` |
| 슬롯 매칭 / bbox 안정화 | `src/tracking/slot.py` |
| 화면에 그리는 색상·레이아웃 | `src/visual/annotator.py` |
| 영상 FPS / 구간 설정 | `scripts/infer_video.py` → `PipelineConfig.target_fps / start_sec / end_sec` |
| 영상 읽기/쓰기 방식 | `src/utils/video_conversion.py` |

---

## 전체 파이프라인 흐름

```
VideoReader (FPS stride)
    ↓
YOLO 탐지  →  person_on / person_off / screen_off
    ↓
슬롯 매칭  →  Hungarian algorithm (기존 슬롯 재사용 or 신규 생성)
    ↓
OCR        →  썸네일 하단에서 이름 읽기 (다수결 투표로 확정)
    ↓
FaceMesh   →  EAR / MAR / pitch_like / tilt_deg / face_center_y
    ↓
졸음 판별  →  Level1(EAR+보조) → Level2(얼굴위치) → Level3(모션hold)
    ↓
시각화     →  바운딩박스 + info box 오버레이
    ↓
VideoWriter + CSV 저장
```

---

## 졸음 감지 알고리즘 수정 방법

YOLO / OCR / FaceMesh는 건드리지 않아도 됩니다.
FaceMesh가 뽑은 신호(EAR, MAR, pitch 등)를 **어떻게 판단할지**만 바꾸면 됩니다.

### Case 1. 임계값 숫자만 바꾸는 경우

`scripts/infer_video.py`의 `DrowsinessConfig`만 수정합니다.

```python
drowsiness=DrowsinessConfig(
    ear_ratio=0.72,           # 기본값 0.75 → 더 민감하게
    tilt_deg_thresh=20.0,     # 기본값 15.0 → 덜 민감하게
    mar_init_abs=0.62,        # 기본값 0.60
    ear_hold_strong_sec=0.3,  # 기본값 0.5 → 더 빠르게 진입
)
```

### Case 2. 판단 로직 자체를 바꾸는 경우 (알고리즘 교체)

수정할 파일이 두 개입니다.

**① `src/detection/drowsiness.py`** — 판단 함수 수정

`update_drowsiness_state()` 안의 로직을 교체합니다.
함수 시그니처(입력/출력)는 그대로 유지해야 파이프라인이 그대로 동작합니다.

```python
# 반드시 이 형태를 유지
def update_drowsiness_state(slot, face_result, motion, cls_name, fps, ts, cfg):
    ...
    return raw_state, final_state, drowsy_reason  # 이 반환값 형태 유지
```

**② `src/tracking/slot.py`** — 알고리즘에 필요한 상태 필드 추가/수정

새 알고리즘이 프레임 간에 기억해야 할 값이 있으면 `SlotState`에 필드를 추가합니다.

```python
# 예: 점수 합산 방식으로 교체하는 경우
@dataclass
class SlotState:
    ...
    # 기존 카운터 필드 대신
    drowsy_score: float = 0.0
    recover_score: float = 0.0
```

---

## 졸음 상태 정의

| 상태 | 조건 |
|---|---|
| `NORMAL` | 기본 상태 |
| `DROWSY` | EAR 낮음 지속 + 보조 신호 조합 (Level1~3) |
| `ABSENT` | `person_off` 또는 `screen_off` 일정 시간 지속 |
| `IGNORE` | 강사로 판별된 슬롯 |

---

## 주요 설정값 위치 (`PipelineConfig` in `scripts/infer_video.py`)

```python
config = PipelineConfig(
    target_fps=10.0,           # 처리 FPS (원본보다 낮게 설정 시 서브샘플링)
    start_sec=0, end_sec=120,  # 처리 구간
    teacher_names=["강경미"],  # 강사 이름 (IGNORE 처리)
    yolo_conf=0.10,            # YOLO 탐지 신뢰도 임계값
    drowsiness=DrowsinessConfig(
        ear_hold_strong_sec=0.5,   # EAR + 보조 → DROWSY 진입까지 지속 시간
        ear_hold_weak_sec=1.5,     # EAR 단독 → DROWSY 진입까지 지속 시간
        ear_ratio=0.75,            # 기준선 대비 EAR 감소 비율
    ),
)
```
