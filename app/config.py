from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"

# 발표용 배경 미디어
# 기본값은 mp4 영상으로 두고, 필요하면 png/jpg로 바꿔도 동작하도록 구성
STAGE_MEDIA_PATH = ASSETS_DIR / "demo_bg.mp4"

# 발표용 배경 원본 해상도
BG_W = 1920
BG_H = 1080

# 3번째 학생 슬롯 위치
SLOT_X = 1724
SLOT_Y = 450
SLOT_W = 180
SLOT_H = 180

APP_TITLE = "온라인 수업 졸음 감지 시스템"
APP_SUBTITLE = "실시간 AI 기반 수강생 상태 모니터링 데모"
