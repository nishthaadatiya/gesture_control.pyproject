
import cv2


def draw_bar(frame, value, x, y, label, color=(0, 200, 120)):
    bar_h = int(200 * value / 100)
    cv2.rectangle(frame, (x, y), (x + 30, y + 200), (50, 50, 50), 2)
    cv2.rectangle(frame,
        (x, y + 200 - bar_h), (x + 30, y + 200), color, cv2.FILLED)
    cv2.putText(frame, f'{label}: {value}%',
        (x - 10, y + 220), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)


def draw_pinch_line(frame, landmarks, color=(255, 255, 0)):
    if len(landmarks) > 8:
        cv2.line(frame, landmarks[4], landmarks[8], color, 2)
        cv2.circle(frame, landmarks[4], 8, color, cv2.FILLED)
        cv2.circle(frame, landmarks[8], 8, color, cv2.FILLED)
