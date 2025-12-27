import time
import cv2
from PySide6.QtCore import QObject, Slot
import mediapipe as mp

class PostureChecker(QObject):
    start_time = None
    sensitivity = None
    default_posture = None

    @Slot(int, int)
    def set_init_variables(self, sensitivity, default_posture):
        self.start_time = time.time()
        self.sensitivity = sensitivity/100
        self.default_posture = default_posture

    def get_mp_frame(self, frame):
        """
        return Image obj usable by MediaPipe
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        mp_frame = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )
        return mp_frame

    def get_posture_value(self, detection_result):
        people_world_landmarks = detection_result.pose_world_landmarks
        if len(people_world_landmarks) == 0:  # No person detected
            return
        wl = people_world_landmarks[0]  # Landmarks of person in frame
        nose = wl[0].y
        shoulder_R = wl[11].y
        shoulder_L = wl[12].y
        shoulder_mid = (shoulder_L + shoulder_R) / 2  # Midpoint height
        return shoulder_mid - nose  # Horizontal Diff

    def check_bad_posture(self, horizontal_difference):
        if horizontal_difference < self.default_posture * self.sensitivity:
            return True
        return False




