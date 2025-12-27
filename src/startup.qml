import QtQuick
import QtQuick.Window
import QtQuick.Controls

Item {
    ApplicationWindow {
        id: menu
        width: 512
        height: 384
        visible: true
        title: "Startup Menu"
        color: "white"

        flags: Qt.WindowStaysOnTopHint

        property int default_posture_value: 1

        Button {
            id: start
            y: Window.height * 0.85
            anchors.horizontalCenter: parent.horizontalCenter
            text: "Start"
            font.pixelSize: 16
            width: 48
            height: 24

            background: Rectangle {
                anchors.fill: parent
                color: Button.pressed ? "red" : "black"
                radius: 4
            }

            onClicked: {
                controller.request_start()
                close()
            }
        }

        Text {
            id: sensitivity
            text: "Sensitivity: " + sensitivitySlider.value.toFixed(0) + "%"
            y: Window.height * 0.70
            anchors.horizontalCenter: parent.horizontalCenter
            font.pointSize: 16
            }

        Slider {
            id: sensitivitySlider
            y: Window.height * 0.75
            anchors.horizontalCenter: parent.horizontalCenter
            width: 384
            from: 0.0
            to: 100.0
            value: 75.0
            stepSize: 1.0

            onValueChanged: {
                console.log("New value:", value);
            }
        }
    }

    Window {
        id: popup
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
                popup.visible = Window.Windowed
            }

            function onHideWindow() {
                console.log("hide")
                popup.visible = false
            }
        }
    }
}