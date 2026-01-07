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
            controller.set_default_posture_value()
            startup.visibility = Window.Minimized
        }

        function onFrameUpdated() {
            if (!webcam.frameReady) {
                webcam.frameReady = true
            }
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

    onVisibilityChanged: (vis) => {
        if (vis === Window.Windowed) {
            controller.set_displaying()
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
            property bool frameReady: false
            source: frameReady ? "image://frames/live" : ""
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
        scale: setArea.pressed ? 1 : hovered ? 1.1 : 1

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
            id: setArea
            anchors.fill: parent
            hoverEnabled: true
            onClicked: {
                controller.set_default_posture_value()
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
        scale: startArea.pressed ? 1 : hovered ? 1.1 : 1

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
            id: startArea
            anchors.fill: parent
            hoverEnabled: true
            onClicked: {
                controller.set_running()
                controller.request_start()
                debug.text = "Mode: Running"
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
        width: xBorder * 12
        height: yBorder * 2/3
        anchors.horizontalCenter: parent.horizontalCenter
        y: parent.height - (yBorder*(3/2) + height + sensitivity.height)
        from: 0.0
        to: 100.0
        value: 75.0
        stepSize: 1.0
        hoverEnabled: true

        background: Rectangle {
            height: yBorder / 4
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            color: "black"
            radius: 4
        }

        handle: Rectangle {
            id: handleRect
            width: xBorder * 2/3
            height: yBorder * 2/3
            radius: xBorder * 2/3
            color: "black"
            transformOrigin: Item.Center

            scale: sensitivitySlider.pressed ? 1 : sensitivitySlider.hovered ? 1.2 : 1

            x: sensitivitySlider.visualPosition * (sensitivitySlider.width - width)
            y: (sensitivitySlider.height - height) / 2

            Behavior on scale {
                NumberAnimation { duration: 150; easing.type: Easing.OutQuad }
            }
        }

        onValueChanged: {
            controller.set_sensitivity(value)
        }
    }
}