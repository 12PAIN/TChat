import os
import sys

from PyQt5 import uic, QtCore
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCloseEvent, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QSizePolicy


class MailViewFormTemplate(QWidget):
    closing = pyqtSignal()

    def closeEvent(self, event: QCloseEvent):
        self.closeCallback()
        self.closing.emit()

    def __init__(self, emailAddress, emailText, objName, closeCallback, imageBinaryData=None, imageExtension=None):
        super().__init__()
        self.closeCallback = closeCallback

        if imageBinaryData is None:
            uic.loadUi('uiTemplates/mailViewForm/mailFormTemplate.ui', self)
        else:
            uic.loadUi('uiTemplates/mailViewForm/mailFormWithImageTemplate.ui', self)
            self.image_label: QLabel = self.image_label


            file_name = f'tmp/tmpImage.{imageExtension}'

            f = open(file_name, 'a')
            f.close()

            with open(file_name, 'wb') as file:
                file.write(imageBinaryData)

            scaled = QPixmap(file_name).scaled(self.image_label.width(), self.image_label.height(),
                                               aspectRatioMode=Qt.KeepAspectRatio)

            self.image_label.setPixmap(scaled)



            os.remove(file_name)


        self.setObjectName('viewEmail_' + objName)
        self.senderEmail.setText(emailAddress)
        self.emailText.setText(emailText)


