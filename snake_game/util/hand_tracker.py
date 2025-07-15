import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.hands_module = mp.solutions.hands
        self.hands = self.hands_module.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.drawing = mp.solutions.drawing_utils

    def get_index_finger_position(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            h, w, _ = frame.shape
            index_finger_tip = hand_landmarks.landmark[self.hands_module.HandLandmark.INDEX_FINGER_TIP]
            cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
            return (cx, cy)
        return None

    def draw_hand(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.drawing.draw_landmarks(frame, hand_landmarks, self.hands_module.HAND_CONNECTIONS)
        return frame
