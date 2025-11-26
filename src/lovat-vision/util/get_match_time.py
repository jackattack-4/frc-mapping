import cv2
import pytesseract
import re

def detect_timer(video_path):
    cap = cv2.VideoCapture(video_path)
    prev_timer = None

    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        
        roi = frame[60:130, 900:1020]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        config = "--psm 7 -c tessedit_char_whitelist=0123456789:"
        text = pytesseract.image_to_string(thresh, config=config).strip()


        if re.match(r"^\d:\d\d$", text):
            if prev_timer and text != prev_timer:
                print(f"Timer progression detected: {prev_timer} -> {text}")

            prev_timer = text

        print(count)

        count += 1

    cap.release()


def extract_timer_text(frame):
    roi = frame[60:130, 900:1020]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    config = "--psm 7 -c tessedit_char_whitelist=0123456789:."
    text = pytesseract.image_to_string(thresh, config=config)

    return text.strip()

def is_match_timer(text):
    # Matches mm:ss format like 2:15 or 0:15
    return bool(re.match(r"^\d:\d\d$", text))

detect_timer("input-data/2025casf_qm3.mp4")