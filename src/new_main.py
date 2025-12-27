#Imports
import sys
import cv2
import time
import numpy as np
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtCore import QThread
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

from src.posture import PostureChecker
from src.popup import PopupController

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2

#Mediapipe Setup
base_options = python.BaseOptions(model_asset_path="../pose_landmarker.task")
options = vision.PoseLandmarkerOptions(base_options=base_options, running_mode=vision.RunningMode.VIDEO)
pose_detector = vision.PoseLandmarker.create_from_options(options)

#Webcam Setup
# cap = cv2.VideoCapture(0) #0 for default webcam
# if not cap.isOpened(): #No webcam handling
#     print("Error: No webcam found")
#     exit()

#Startup Menu
QApplication.setAttribute(Qt.AA_DontShowIconsInMenus, False)
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
engine = QQmlApplicationEngine()
controller = PopupController()
engine.rootContext().setContextProperty("controller", controller)

# Load the ROOT QML file only
qml_dir = Path(__file__).parent / "qml"
engine.addImportPath(str(qml_dir))
engine.load(str(qml_dir / "main.qml"))

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())

# #Running Loop
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     timestamp_ms = int((time.time() - run_instance.start_time) * 1000)
#     mp_frame = run_instance.get_mp_frame(frame)
#     detection_result = pose_detector.detect_for_video(mp_frame, timestamp_ms=timestamp_ms)
#     posture_value = run_instance.get_posture_value(detection_result)
#     #print(posture_value, run_instance.sensitivity, run_instance.default_posture)
#
#     if run_instance.check_bad_posture(posture_value):
#         window.show()
#     else:
#         window.hide()
#
# # Cleanup
# cap.release()