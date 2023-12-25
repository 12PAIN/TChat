import sys

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget


class MailWidgetTemplate(QWidget):
    clicked = QtCore.pyqtSignal()

    def __init__(self, emailAddress, emailText, objName):
        super().__init__()
        uic.loadUi('uiTemplates/mailPreviewTemplate/mailPreviewTemplate.ui', self)
        self.setObjectName(objName)
        self.emailAddress.setText(emailAddress)
        self.emailText.setText(emailText[:40])
        self.header.setText(emailAddress[:2].upper())

    def mouseReleaseEvent(self, QMouseEvent):
        self.clicked.emit()
