from PySide6.QtCore import QObject, Signal, Slot
import time
import capture, posture, image

def get_capture_frame():
    frame = capture.get_frame()
    timestamp_ms = capture.get_timestamp_ms()
    rgb_frame = capture.get_rgb_frame(frame)
    return rgb_frame, timestamp_ms

def get_posture_frame(rgb_frame, timestamp_ms):
    mp_frame = posture.get_mp_frame(rgb_frame)
    detection_result = posture.get_detection_result(mp_frame, timestamp_ms)
    posture_value = posture.get_posture_value(detection_result)
    return posture_value

class BackgroundWorker(QObject):
    frameReady = Signal(object) # np.ndarray
    postureBad = Signal()
    postureGood = Signal()
    finished = Signal()

    def __init__(self):
        super().__init__()
        self._running = True

    @Slot()
    def run(self):
        while self._running:
            rgb_frame, timestamp_ms = get_capture_frame()
            mp_frame = posture.get_mp_frame(rgb_frame)
            detection_result = posture.get_detection_result(mp_frame, timestamp_ms)
            posture_value = posture.get_posture_value(detection_result)
            if posture_value <= posture.default_posture_value * posture.sensitivity:
                self.postureBad.emit() # Bad Posture
            else:
                self.postureGood.emit() # Good Posture

            annotated_frame = posture.draw_landmarks_on_image(rgb_frame, detection_result)
            #bgr_annotated_frame = capture.get_bgr_frame(annotated_frame)
            qimage = image.get_qimage(annotated_frame)
            self.frameReady.emit(qimage)

            time.sleep(0.1)

        capture.cleanup()
        self.finished.emit()
        self.stop()

    @Slot()
    def stop(self):
        self._running = False