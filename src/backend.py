#Imports
from PySide6.QtCore import QObject, Signal, Slot

import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.cc.vision import pose_detector
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2

import posture
import capture

#Handles all communication between main.py and QML
class QMLController(QObject):
    endMenu = Signal()
    startProgram = Signal()
    showWindow = Signal()
    hideWindow = Signal()

    @Slot()
    def request_start(self):
        self.endMenu.emit()
        self.startProgram.emit()

    @Slot()
    def request_show(self):
        self.showWindow.emit()

    @Slot()
    def request_hide(self):
        self.hideWindow.emit()

    @Slot(int)
    def set_sensitivity(self, value):
        posture.sensitivity = value

    @Slot(float)
    def set_default_posture_value(self, value):
        posture.default_posture_value = value

    @Slot()
    def detect_frame(self):
        frame = capture.get_frame()
        if type(frame) == bool:
            return None
        timestamp_ms = capture.get_timestamp_ms()
        RGB_frame = capture.get_RGB_frame(frame)
        mp_frame = posture.get_mp_frame(RGB_frame)
        detection_result = posture.get_detection_result(mp_frame, timestamp_ms)
        return detection_result

    @Slot()
    def run_main(self):
        print("Running main loop")
        while True:
            detection_result = self.detect_frame()
            if not detection_result:
                break

            posture_value = posture.get_posture_value(detection_result)
            if posture_value <= posture.default_posture_value * posture.sensitivity:
                print("Bad Posture")  # Bad Posture
            else:
                print("Good Posture")  # Good Posture

        capture.cleanup()

