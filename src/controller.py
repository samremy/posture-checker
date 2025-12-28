#Handles all communication between main.py and QML
from PySide6.QtCore import QObject, Signal, Slot

class QMLController(QObject):
    #startProgram = Signal()

    @Slot()
    def request_start(self):
        #self.startProgram.emit()
        print("Program starting")