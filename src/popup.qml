import QtQuick
import QtQuick.Window
import QtQuick.Controls

Window {
    id: root
    width: 192
    height: 64
    visible: true
    title: "Posture warning"
    color: "red"

    flags: Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint

    x: Screen.virtualX
    y: Screen.virtualY

    Text {
        anchors.centerIn: parent
        text: "FIX POSTURE"
        color: "white"
        font.pixelSize: 24
    }

    Connections {
        target: controller

        function onShowWindow() {
            console.log("show")
            root.visible = Window.Windowed
        }

        function onHideWindow() {
            console.log("hide")
            root.visible = false
        }
    }
}
