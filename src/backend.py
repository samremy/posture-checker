#Imports
from PySide6.QtCore import QObject, Signal, Slot, QThread
import posture, capture
from worker import get_capture_frame, get_posture_frame, BackgroundWorker

#Handles all communication between main.py and QML
class QMLController(QObject):
    startProgram = Signal()
    endMenu = Signal()
    frameUpdated = Signal()
    postureBad = Signal()
    showWindow = Signal()
    hideWindow = Signal()

    def __init__(self, frame_provider):
        super().__init__()
        self.thread = None
        self.worker = None
        self.frame_provider = frame_provider
        self.start_worker()

    @Slot()
    def request_show(self):
        self.showWindow.emit()

    @Slot()
    def request_hide(self):
        self.hideWindow.emit()

    @Slot(object)
    def draw_frame(self, frame):
        capture.draw_frame(frame)

    @Slot(object)
    def update_frame(self, image):
        self.frame_provider.set_image(image)
        print("Image set, emitting frameUpdated")
        self.frameUpdated.emit()

    @Slot(int)
    def set_sensitivity(self, value):
        posture.sensitivity = value / 100

    @Slot()
    def set_default_posture_value(self):
        rgb_frame, timestamp_ms = get_capture_frame()
        posture_value = get_posture_frame(rgb_frame, timestamp_ms)
        posture.default_posture_value = posture_value

    @Slot()
    def request_start(self):
        self.endMenu.emit()

    def start_worker(self):
        self.thread = QThread()
        self.worker = BackgroundWorker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.frameReady.connect(self.update_frame) # self.draw_frame

        self.worker.postureBad.connect(self.showWindow)
        self.worker.postureGood.connect(self.hideWindow)

        self.thread.start()
