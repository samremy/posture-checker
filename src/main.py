#Imports
import os
import sys

from backend import QMLController

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

#Make startup window show
app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

script_dir = os.path.dirname(os.path.abspath(__file__))
menu_qml_file_path = os.path.join(script_dir, "qml", "startup_menu.qml")
popup_qml_file_path = os.path.join(script_dir, "qml", "popup_warning.qml")

controller = QMLController()
engine.rootContext().setContextProperty("controller", controller)

engine.load(str(menu_qml_file_path))
engine.load(str(popup_qml_file_path))

if not engine.rootObjects():
    sys.exit(-1)

app.exec()