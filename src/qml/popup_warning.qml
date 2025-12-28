//Popup warning window. Appears when posture triggers
import QtQuick
import QtQuick.Window

Window {
    Component.onCompleted: {
        console.log("Popup created")
    }

    id: popup
    visible: false
    width: 192
    height: 64
    title: "Posture warning"
    color: "red"

    flags: Qt.Tool | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint

    x: Screen.virtualX
    y: Screen.virtualY

    Connections {
        target: controller

        function onStartProgram() {
            console.log("Requesting to run main")
            controller.run_main()
        }

        function onShowWindow() {
            console.log("Showing popup")
            popup.visible = true
        }

        function onHideWindow() {
            console.log("Hiding popup")
            popup.visible = false
        }
    }

    Text {
        anchors.centerIn: parent
        text: "FIX POSTURE"
        color: "white"
        font.pixelSize: 24
    }
}