import cv2
import json
import os
import mediapipe as mp


# Load config
_config_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(_config_path) as f:
    _cfg = json.load(f)


class HandDetector:
    def __init__(self, max_hands=2):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=_cfg["detection_conf"],
            min_tracking_confidence=_cfg["tracking_conf"],
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, frame, draw=True):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)
        if self.results.multi_hand_landmarks and draw:
            for lm in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, lm, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def get_landmarks(self, frame, hand_index=0):
        """Returns list of (x, y) pixel coords for 21 landmarks."""
        landmarks = []
        if self.results.multi_hand_landmarks:
            if hand_index < len(self.results.multi_hand_landmarks):
                h, w, _ = frame.shape
                for lm in self.results.multi_hand_landmarks[hand_index].landmark:
                    landmarks.append((int(lm.x * w), int(lm.y * h)))
        return landmarks

    def is_fist(self, landmarks):
        """Detect fist: all five fingertips below their respective knuckles.

        Fingertips (4, 8, 12, 16, 20) are compared against their
        PIP / IP joints (3, 6, 10, 14, 18).  'Below' means a larger
        y-value in image coordinates.
        """
        if len(landmarks) < 21:
            return False
        tips     = [4,  8,  12, 16, 20]
        knuckles = [3,  6,  10, 14, 18]
        return all(landmarks[t][1] > landmarks[k][1]
                   for t, k in zip(tips, knuckles))

    def get_handedness(self):
        """Returns list of Left or Right for each detected hand."""
        sides = []
        if self.results.multi_handedness:
            for hand_info in self.results.multi_handedness:
                sides.append(hand_info.classification[0].label)
        return sides
