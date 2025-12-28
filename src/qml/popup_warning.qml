//Popup warning window. Appears when posture triggers
import QtQuick
import QtQuick.Window

Window {
    Component.onCompleted: {
        console.log("✅ popup created")
    }

    visible: true
    width: 192
    height: 64
    title: "Posture warning"
    color: "red"

    flags: Qt.Tool | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint

    x: Screen.virtualX
    y: Screen.virtualY

    Text {
        anchors.centerIn: parent
        text: "FIX POSTURE"
        color: "white"
        font.pixelSize: 24
    }
}