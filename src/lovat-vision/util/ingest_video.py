import cv2
import os
import json

from constants import GamePhase

import pytesseract

def ingest_video(video_path, match_id, output_dir="frames", fps_target=10):
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    match_dir = os.path.join(output_dir, f"match_{match_id}")
    os.makedirs(match_dir, exist_ok=True)

    frame_interval = int(fps / fps_target)
    frame_count = 0
    saved_count = 0

    phase = GamePhase.PRE_MATCH

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        
        roi = frame[60:130, 900:1020]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        config = "--psm 7 -c tessedit_char_whitelist=0123456789:"
        text = pytesseract.image_to_string(thresh, config=config).strip()

        match (phase):
            case GamePhase.PRE_MATCH:
                if text == "0:14":
                    phase = GamePhase.AUTO
                    matchStartFrame = frame_count - 1
                    print("AUTO")
            case GamePhase.AUTO:
                if text == "2:15":
                    phase = GamePhase.TRANSITION
                    print("TRANSITION")
            case GamePhase.TRANSITION:
                if text == "2:14":
                    phase = GamePhase.TELEOP
                    print("TELEOP")
            case GamePhase.TELEOP:
                if text == "0:20":
                    phase = GamePhase.ENDGAME
                    print("ENDGAME")
            case GamePhase.ENDGAME:
                if text == "0:00":
                    phase = GamePhase.POST_MATCH
                    print("POST_MATCH")
        
        if frame_count % frame_interval == 0:
            timestamp = frame_count / fps
            filename = f"frame_{saved_count:06d}_{timestamp:.2f}_{text}.jpg"
            path = os.path.join(match_dir, filename)
            cv2.imwrite(path, frame)
            saved_count += 1

        frame_count += 1

    cap.release()

    metadata = {
        "match_id": match_id,
        "original_fps": fps,
        "target_fps": fps_target,
        "duration": duration,
        "resolution": f"{width}x{height}",
        "frames_extracted": saved_count,
        "match_start": matchStartFrame
    }

    with open(f"{match_dir}/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    return metadata


print(ingest_video("input-data/2025casf_qm3.mp4", "2025casf_qm3"))