import cv2
import os

def extract_frames_video(video_path, output_dir, interval_sec=1, prefix=None):
    """
    영상(mp4)에서 일정 간격으로 프레임을 추출하는 함수

    Args:
        video_path (str): 영상 파일 경로
        output_dir (str): 프레임 저장 폴더
        interval_sec (int): 몇 초마다 프레임 추출할지 (default=1초)
        prefix (str): 저장 파일명 접두사 (default: None → 영상 파일명 사용)
    """

    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))

    if prefix is None:
        prefix = os.path.splitext(os.path.basename(video_path))[0]

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_sec)

    frame_id = 0
    saved_id = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % frame_interval == 0:
            save_path = os.path.join(output_dir, f"{prefix}_frame_{saved_id}.jpg")
            cv2.imwrite(save_path, frame)
            saved_id += 1

        frame_id += 1

    cap.release()
    print(f"총 {saved_id}개의 프레임 저장")


def extract_frames_from_folder(input_dir, output_root, interval_sec=1):
    """
    폴더 내 모든 mp4 영상을 순회하며 프레임을 추출하는 함수

    Args:
        input_dir (str or Path): 영상이 들어있는 폴더
        output_root (str or Path): 프레임을 저장할 루트 폴더
        interval_sec (float): 몇 초마다 프레임을 추출할지
    """

    for file_name in os.listdir(input_dir):
        if not file_name.lower().endswith(".mp4"):
            continue

        video_path = os.path.join(input_dir, file_name)
        video_name = os.path.splitext(file_name)[0]
        output_dir = os.path.join(output_root, video_name)

        print(f"Processing: {file_name}")
        extract_frames_video(video_path, output_dir, interval_sec)