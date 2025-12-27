from PySide6.QtCore import QObject, Signal, Slot

class PopupController(QObject):
    startProgram = Signal()
    showWindow = Signal()
    hideWindow = Signal()

    @Slot()
    def request_start(self):
        self.startProgram.emit()
        print("Start Requested")

    @Slot()
    def request_show(self):
        self.showWindow.emit()

    @Slot()
    def request_hide(self):
        self.hideWindow.emit()