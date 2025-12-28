//startup menu window. Appears on initialization
import QtQuick
import QtQuick.Window
import QtQuick.Controls

Window {
    id: startup
    visible: true
    width: 512
    height: 384
    title: "Startup menu"
    color: "white"

    Connections {
        target: controller

        function onEndMenu() {
            controller.set_sensitivity(sensitivitySlider.value.toFixed(0))
            controller.set_default_posture_value()
            startup.visible = false
        }
    }

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
    }
}