import cv2
import time
import numpy as np

from pose_handler import PoseHandler
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QImage

class VideoWorker(QObject):
    frameReady = Signal(QImage)

    def start(self):
        START_TIME = time.time()
        cap = cv2.VideoCapture(0) #0 for default webcam
        if not cap.isOpened(): #No webcam handling
            print("Error: No webcam found")
            exit()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            timestamp_ms = int((time.time() - START_TIME) * 1000)  # Time since init in ms
            mp_frame = PoseHandler.get_mp_frame(frame)

            default_posture_value = PoseHandler.get_posture_value(detection_result)
            detection_result = PoseHandler.pose_detector.detect_for_video(mp_frame, timestamp_ms=timestamp_ms)

            frame_with_landmarks = PoseHandler.draw_landmarks_on_image(frame.copy(), detection_result)

            h, w, ch = frame_with_landmarks.shape
            bytes_per_line = ch * w

            image = QImage(
                rgb.data,
                w,
                h,
                bytes_per_line,
                QImage.Format_RGB888
            ).copy()

            self.frameReady.emit(image)

        cap.release()