#Imports
from PySide6.QtCore import QObject, Signal, Slot, QThread
import posture
from worker import get_frame_value, BackgroundWorker

#Handles all communication between main.py and QML
class QMLController(QObject):
    startProgram = Signal()
    endMenu = Signal()
    showWindow = Signal()
    hideWindow = Signal()

    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None

    @Slot()
    def request_show(self):
        self.showWindow.emit()

    @Slot()
    def request_hide(self):
        self.hideWindow.emit()

    @Slot(int)
    def set_sensitivity(self, value):
        posture.sensitivity = value / 100

    @Slot()
    def set_default_posture_value(self):
        posture_value = get_frame_value()
        posture.default_posture_value = posture_value

    @Slot()
    def request_start(self):
        self.endMenu.emit()
        self.start_worker()

    def start_worker(self):
        self.thread = QThread()
        self.worker = BackgroundWorker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.postureBad.connect(self.showWindow)
        self.worker.postureGood.connect(self.hideWindow)

        self.thread.start()
