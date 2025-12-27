import sys
import cv2
import time

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

import pose_handler as ph
import frame_handler as fh

#Define Constants
START_TIME = time.time() #Time on init

#Posture to overwrite
default_posture_value = 1
sensitivity = 0.75


app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
controller = fh.AppController()
engine.rootContext().setContextProperty("controller", controller)
engine.load("popup.qml")

if not engine.rootObjects():
    sys.exit(-1)

#Running loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    timestamp_ms = int((time.time() - START_TIME) * 1000) #Time since init in ms

    mp_frame = ph.get_mp_frame(frame)
    detection_result = ph.pose_detector.detect_for_video(mp_frame, timestamp_ms=timestamp_ms)

    if cv2.waitKey(1) & 0xFF == ord('s'): #Set default value on s keypress
        default_posture_value = ph.get_posture_value(detection_result)

    elif default_posture_value != 1: #Default posture has been set
        posture_value = ph.get_posture_value(detection_result)
        if posture_value <= default_posture_value * sensitivity: #Bad Posture
            controller.showWindow.emit()
        else: #Good Posture
            controller.hideWindow.emit()

    frame_with_landmarks = ph.draw_landmarks_on_image(frame.copy(), detection_result)

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
    #cv2.imshow("Pose Detection", frame_with_landmarks)

    #Break on "q" keypress
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()