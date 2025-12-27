import sys
import cv2
import time
from PySide6.QtCore import QThread
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from src.popup import PopupController
from src.posture import PostureChecker


class VideoWorker(QThread):
    def __init__(self, controller, checker):
        super().__init__()
        self.controller = controller
        self.checker = checker
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(0)

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            posture_value = self.checker.process(frame)

            if self.checker.check_bad_posture(posture_value):
                self.controller.showWindow.emit()
            else:
                self.controller.hideWindow.emit()

        cap.release()
