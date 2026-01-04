#Imports
from PySide6.QtCore import QObject, Signal, Slot, QThread
import posture, capture
from worker import get_capture_frame, get_posture_frame, BackgroundWorker

#Handles all communication between main.py and QML
class QMLController(QObject):
    startProgram = Signal()
    endMenu = Signal()
    frameUpdated = Signal()
    showWindow = Signal()
    hideWindow = Signal()
    goodPosture = Signal()
    badPosture = Signal()

    def __init__(self, frame_provider):
        super().__init__()
        self.displaying = True
        self.mode = 0 #Enum: 0 Setup, 1 Detecting, 2 Running
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

    def good_posture(self):
        if not self.displaying:
            self.hideWindow.emit()
        elif self.mode != 0:
            self.goodPosture.emit()

    def bad_posture(self):
        if not self.displaying:
            self.showWindow.emit()
        elif self.mode != 0:
            self.badPosture.emit()

    @Slot(object)
    def draw_frame(self, frame):
        capture.draw_frame(frame)

    @Slot(object)
    def update_frame(self, image):
        if self.displaying:
            self.frame_provider.set_image(image)
            self.frameUpdated.emit()

    @Slot(int)
    def set_sensitivity(self, value):
        posture.sensitivity = value / 100

    @Slot()
    def set_default_posture_value(self):
        rgb_frame, timestamp_ms = get_capture_frame()
        posture_value = get_posture_frame(rgb_frame, timestamp_ms)
        posture.default_posture_value = posture_value
        if not self.mode == 1:
            self.mode = 1

    @Slot()
    def set_displaying(self):
        self.displaying = True
        self.hideWindow.emit()

    @Slot()
    def set_detecting(self):
        self.mode = 1 # Detecting

    @Slot()
    def set_running(self):
        self.mode = 2 # Running

    @Slot()
    def request_start(self):
        self.endMenu.emit()
        self.displaying = False

    def start_worker(self):
        self.thread = QThread()
        self.worker = BackgroundWorker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.frameReady.connect(self.update_frame)

        self.worker.postureGood.connect(self.good_posture)
        self.worker.postureBad.connect(self.bad_posture)

        self.thread.start()
