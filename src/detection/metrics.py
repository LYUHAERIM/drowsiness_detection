import numpy as np

# MediaPipe Face Mesh 랜드마크 인덱스
# https://github.com/google/mediapipe/blob/master/mediapipe/modules/face_geometry/data/canonical_face_model_uv_visualization.png
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33,  160, 158, 133, 153, 144]
_MOUTH_TOP   = 13   # 윗입술 중앙
_MOUTH_BOT   = 14   # 아랫입술 중앙
_MOUTH_LEFT  = 78   # 왼쪽 입꼬리
_MOUTH_RIGHT = 308  # 오른쪽 입꼬리


def _dist(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


def ear(landmarks_px: np.ndarray, eye_indices: list[int]) -> float:
    """
    Eye Aspect Ratio (눈 종횡비)
    - 0에 가까울수록 눈이 감긴 상태
    """
    p = landmarks_px[eye_indices]
    vertical = (_dist(p[1], p[5]) + _dist(p[2], p[4])) / 2
    horizontal = _dist(p[0], p[3])
    return vertical / (horizontal + 1e-6)


def mar(landmarks_px: np.ndarray) -> float:
    """
    Mouth Aspect Ratio (입 종횡비)
    - 0에 가까울수록 입이 닫힌 상태, 클수록 입이 벌어진 상태 (하품)
    """
    vertical   = _dist(landmarks_px[_MOUTH_TOP], landmarks_px[_MOUTH_BOT])
    horizontal = _dist(landmarks_px[_MOUTH_LEFT], landmarks_px[_MOUTH_RIGHT])
    return vertical / (horizontal + 1e-6)


def head_pose(landmarks: np.ndarray) -> tuple[float, float]:
    """
    고개 방향 추정 (pitch, yaw) - 단위: 도(degree)
    - pitch > 0: 고개 숙임 / < 0: 고개 젖힘
    - yaw   > 0: 오른쪽 / < 0: 왼쪽

    Args:
        landmarks: 정규화 좌표 (N, 3)
    """
    nose     = landmarks[1, :2]
    forehead = landmarks[10, :2]
    chin     = landmarks[152, :2]
    l_eye    = landmarks[263, :2]
    r_eye    = landmarks[33, :2]

    # pitch: 이마→턱 수직선에서 코의 수평 이탈 정도
    face_dir = chin - forehead
    face_len = np.linalg.norm(face_dir) + 1e-6
    pitch = float(np.degrees(np.arctan2(-face_dir[1], face_len)))

    # yaw: 양 눈 중심 대비 코의 수평 이탈 정도
    eye_mid  = (l_eye + r_eye) / 2
    eye_dist = np.linalg.norm(l_eye - r_eye) + 1e-6
    yaw = float(np.degrees(np.arctan2(nose[0] - eye_mid[0], eye_dist)))

    return pitch, yaw


def left_ear(landmarks_px: np.ndarray) -> float:
    return ear(landmarks_px, LEFT_EYE)


def right_ear(landmarks_px: np.ndarray) -> float:
    return ear(landmarks_px, RIGHT_EYE)


def mean_ear(landmarks_px: np.ndarray) -> float:
    return (left_ear(landmarks_px) + right_ear(landmarks_px)) / 2
