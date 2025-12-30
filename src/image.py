from PySide6.QtQuick import QQuickImageProvider
from PySide6.QtGui import QImage
from PySide6.QtCore import Qt

def get_qimage(rgb_frame):
    h, w, ch = rgb_frame.shape
    return QImage(
        rgb_frame.data,
        w,
        h,
        ch * w,
        QImage.Format_RGB888
    ).copy()  # memory safety

class FrameProvider(QQuickImageProvider):
    def __init__(self):
        super().__init__(QQuickImageProvider.Image)
        self.image = QImage()

    def set_image(self, image: QImage):
        self.image = image

    def requestImage(self, id, size, requestedSize):
        if size is not None:
            size.setWidth(self.image.width())
            size.setHeight(self.image.height())
        return self.image