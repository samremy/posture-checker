from PySide6.QtCore import QObject, Signal, Slot
import time
import capture, posture

def get_frame_posture_value():
    frame = capture.get_frame()
    timestamp_ms = capture.get_timestamp_ms()
    RGB_frame = capture.get_RGB_frame(frame)

    mp_frame = posture.get_mp_frame(RGB_frame)
    detection_result = posture.get_detection_result(mp_frame, timestamp_ms)
    posture_value = posture.get_posture_value(detection_result)

    return posture_value

class BackgroundWorker(QObject):
    postureBad = Signal()
    postureGood = Signal()
    finished = Signal()

    def __init__(self):
        super().__init__()
        self._running = True

    @Slot()
    def run(self):
        print("Running main loop")
        while self._running:
            posture_value = get_frame_posture_value()
            print("Posture Value: ", posture_value, "Default x Sensitivity: ", posture.default_posture_value * posture.sensitivity)
            if posture_value <= posture.default_posture_value * posture.sensitivity:
                print("Bad Posture")  # Bad Posture
                self.postureBad.emit()
            else:
                print("Good Posture")  # Good Posture
                self.postureGood.emit()

            time.sleep(1)

        capture.cleanup()
        self.finished.emit()

    @Slot()
    def stop(self):
        self._running = False