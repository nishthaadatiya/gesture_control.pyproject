import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, max_hands=2, detection_conf=0.7, tracking_conf=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
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


    def get_handedness(self):
        """Returns list of Left or Right for each detected hand."""
        sides = []
        if self.results.multi_handedness:
            for hand_info in self.results.multi_handedness:
                sides.append(hand_info.classification[0].label)
        return sides

