import QtQml
import QtQuick
import QtQuick.Window
import QtQuick.Controls
import "."

ApplicationWindow {
    id: root
    visible: false   // root window hidden
    width: 1
    height: 1

    Component.onCompleted: {
        console.log("✅ main.qml loaded")
    }

    StartupWindow {
        id: menu
    }

    PopupWindow {
        id: popup
    }

    Connections {
        target: controller

        function onShowWindow() {
            console.log("show")
            popup.visible = true
        }

        function onHideWindow() {
            console.log("hide")
            popup.visible = false
        }
    }
}
