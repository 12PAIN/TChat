from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QLabel, QWidget


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.imageAttached = False

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.imageAttached = True
        self.image_path = event.mimeData().urls()[0].toLocalFile()

        pixmap = QPixmap(self.image_path)

        scaled = pixmap.scaled(self.width(), self.height(),
                               aspectRatioMode=Qt.KeepAspectRatio)

        self.setPixmap(scaled)


class AddImageToMessage(QDialog):

    def __init__(self, parent, imageContentCallback):
        super().__init__(parent)
        self.imageContentCallback = imageContentCallback

        uic.loadUi('uiTemplates/imageAddForm/imageAddForm.ui', self)

        self.buttonBox.accepted.connect(self.saveImageContent)

        self.image_label = ImageLabel(self)
        self.image_label.move(20, 40)
        self.image_label.resize(831, 671)

    def saveImageContent(self):
        if not self.image_label.imageAttached:
            return

        with open(self.image_label.image_path, 'rb') as file:
            image_extension = self.image_label.image_path.split('.')[-1]
            print(image_extension)
            image_data = file.read()
            self.imageContentCallback(image_data, image_extension)
