from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from viewModels.addImageDialog.addImageDialog import AddImageToMessage


class WriteMessageForm(QMainWindow):

    def __init__(self, sendCallback):
        super().__init__()
        self.imageData = None
        self.imageExtension = None
        self.sendCallback = sendCallback

        uic.loadUi('uiTemplates/writeMessageForm/writeMessageForm.ui', self)
        self.sendMessageButton.clicked.connect(self.handleSend)
        self.addImageButton.clicked.connect(self.openImageDialog)

    def openImageDialog(self):
        dialog = AddImageToMessage(self, self.imageContentCallback)
        dialog.exec()

    def imageContentCallback(self, image_data, image_extension):
        self.imageData = image_data
        self.imageExtension = image_extension

    def handleSend(self):

        receiverLogin = self.receiverLoginInput.text()
        messageText = self.messageTextInput.toPlainText().strip()

        if len(receiverLogin) < 5:
            self.statusbar.showMessage("Ошибка! Длина логина не может быть меньше 5 символов!")
            return

        if len(messageText) < 5:
            self.statusbar.showMessage("Ошибка! Длина сообщения не может быть меньше 5 символов!")
            return

        if not self.sendCallback(receiverLogin, messageText, self.imageData, self.imageExtension):
            self.statusbar.showMessage("Ошибка! Пользователя не существует!")
            return