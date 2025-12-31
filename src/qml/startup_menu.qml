//startup menu window. Appears on initialization
import QtQuick
import QtQuick.Window
import QtQuick.Controls

Window {
    id: startup
    visible: true
    width: 512
    height: 384
    property int xBorder: width/24
    property int yBorder: height/18
    title: "Startup menu"
    color: "white"

    Connections {
        target: controller

        function onEndMenu() {
            controller.set_sensitivity(sensitivitySlider.value.toFixed(0))
            controller.set_default_posture_value()
            startup.visible = false
        }

        function onFrameUpdated() {
            webcam.source = "image://frames/live?" + Date.now()
        }

        function onGoodPosture() {
            imageBg.color = "green"
            posture.color = "green"
            posture.text = "Good Posture"
        }

        function onBadPosture() {
            imageBg.color = "red"
            posture.color = "red"
            posture.text = "Bad Posture"
        }
    }

    Rectangle {
        id: imageBg
        color: "black"
        anchors.horizontalCenter: parent.horizontalCenter
        y: yBorder + debug.height
        width: webcam.width + xBorder/4
        height: webcam.height + yBorder/4

        Image {
            id: webcam
            width: parent.parent.width - (xBorder * 2)
            height: width * (9/16)
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            cache: false
            source: "image://frames/live"

            Timer {
                interval: 16   // ~60 FPS
                running: true
                repeat: true
                onTriggered: webcam.source = "image://frames/live?" + Date.now()
            }
        }
    }


    Text {
        id: debug
        text: "Mode: Setup"
        // "Mode: Detecting. Start program
        color: "black"
        font.pixelSize: yBorder * (2/3)
        height: yBorder * (2/3)
        x: xBorder
        y: yBorder * (2/3)
    }

    Text {
        id: posture
        text: "Good Posture"
        color: "green"
        visible: false
        font.pixelSize: yBorder * (2/3)
        font.bold: true
        height: yBorder * (2/3)
        anchors.horizontalCenter: parent.horizontalCenter
        y: yBorder * (2/3)
    }

    Text {
        id: tooltip
        text: "Set default posture"
        color: "black"
        font.pixelSize: yBorder * (2/3)
        height: yBorder * (2/3)
        x: parent.width - (xBorder + contentWidth)
        y: yBorder * (2/3)
    }

    Control {
        id: set
        width: xBorder * 3
        height: yBorder * (3/2)
        x: xBorder
        y: parent.height - (yBorder + height)
        hoverEnabled: true
        scale: hovered ? 1.08 : 1.0

        Behavior on scale {
            NumberAnimation {
                duration: 120
                easing.type: Easing.OutCubic
            }
        }
        contentItem: Text {
            text: "Set"
            font.pixelSize: yBorder * (2/3)
            color: "white"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        background: Rectangle {
            color: "black"
            radius: 4
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onClicked: {
                controller.set_default_posture_value()
                controller.set_sensitivity(sensitivitySlider.value.toFixed(0))
                controller.set_detecting()

                debug.text = "Mode: Detecting"
                posture.visible = true
                tooltip.text = "Start program"
            }
        }
    }

    Control {
        id: start
        width: xBorder * 3
        height: yBorder * (3/2)
        x: parent.width - (xBorder + width)
        y: parent.height - (yBorder + height)
        hoverEnabled: true
        scale: hovered ? 1.08 : 1.0

        Behavior on scale {
            NumberAnimation {
                duration: 120
                easing.type: Easing.OutCubic
            }
        }

        contentItem: Text {
            text: "Start"
            font.pixelSize: yBorder * (2/3)
            color: "white"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        background: Rectangle {
            color: "black"
            radius: 4
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onClicked: {
                controller.request_start()
            }
        }
    }

    Text {
        id: sensitivity
        text: "Sensitivity: " + sensitivitySlider.value.toFixed(0) + "%"
        color: "black"
        font.pixelSize: yBorder * (2/3)
        height: yBorder * (2/3)
        anchors.horizontalCenter: parent.horizontalCenter
        y: parent.height - (yBorder*(1) + height)
    }

    Slider {
        id: sensitivitySlider
        width: 12 * xBorder
        height: yBorder / 4
        anchors.horizontalCenter: parent.horizontalCenter
        y: parent.height - (yBorder*(3/2) + height + sensitivity.height)
        from: 0.0
        to: 100.0
        value: 75.0
        stepSize: 1.0
        hoverEnabled: true

        background: Rectangle {
            color: "black"
            radius: 4
        }

        handle: Rectangle {
            id: handleRect
            width: xBorder * 2/3
            height: yBorder * 2/3
            radius: xBorder * 2/3
            color: "black"

            x: sensitivitySlider.leftPadding +
            sensitivitySlider.visualPosition *
            (sensitivitySlider.availableWidth - width)

            y: sensitivitySlider.topPadding +
            (sensitivitySlider.availableHeight - height) / 2


            //scale: sensitivitySlider.pressed ? 0.9 :
                   //sensitivitySlider.hovered ? 1.15 : 1.0

            Behavior on scale {
                NumberAnimation {
                    duration: 120
                    easing.type: Easing.OutCubic
                }
            }

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                acceptedButtons: Qt.NoButton

                onEntered: handleRect.scale = 1.2
                onExited: handleRect.scale = 1.0
            }
        }

        onValueChanged: {
            controller.set_sensitivity(value)
        }
    }
}