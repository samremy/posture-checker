//Popup warning window. Appears when posture triggers
import QtQuick
import QtQuick.Window

Window {
    id: popup
    visible: false
    width: 192
    height: 64
    title: "Posture warning"
    color: "red"

    flags: Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint

    x: Screen.virtualX
    y: Screen.virtualY

    Connections {
        target: controller

        function onStartProgram() {
            controller.run_main()
        }

        function onShowWindow() {
            if (!popup.visible) {
                popup.visible = true
            }
        }

        function onHideWindow() {
            if (popup.visible) {
                popup.visible = false
            }
        }
    }

    Text {
        anchors.centerIn: parent
        text: "FIX POSTURE"
        color: "white"
        font.pixelSize: 24
    }
}