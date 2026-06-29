import cv2
import json
import os
import numpy as np
from collections import deque
from hand_detector import HandDetector
from controller import pinch_distance, set_volume, set_brightness
from hud import draw_bar, draw_pinch_line


# Load config
_config_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(_config_path) as f:
    cfg = json.load(f)


cap = cv2.VideoCapture(0)
detector = HandDetector(max_hands=2)


# Rolling buffer for smoothing (size from config)
win = cfg["smoothing_window"]
vol_buf = deque(maxlen=win)
bright_buf = deque(maxlen=win)
vol_pct = 50
bright_pct = 50


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # mirror - more natural
    frame = detector.find_hands(frame)
    handedness = detector.get_handedness()

    for i, side in enumerate(handedness):
        lm = detector.get_landmarks(frame, hand_index=i)
        if not lm:
            continue

        # Fist lock — freeze value when fist is detected
        if detector.is_fist(lm):
            continue

        dist = pinch_distance(lm)
        draw_pinch_line(frame, lm)

        if side == "Left":
            vol_buf.append(dist)
            smoothed = float(np.mean(vol_buf))
            vol_pct = set_volume(smoothed)
        elif side == "Right":
            bright_buf.append(dist)
            smoothed = float(np.mean(bright_buf))
            bright_pct = set_brightness(smoothed)

    draw_bar(frame, vol_pct,    x=20,  y=50,
           label="Vol",   color=(0, 200, 120))
    draw_bar(frame, bright_pct, x=600, y=50,
           label="Bright", color=(0, 180, 255))

    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
