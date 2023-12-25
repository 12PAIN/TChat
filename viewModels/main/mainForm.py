import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QScrollArea, QWidget
from templateModels.emailPreview.emailMessagePreviewTemplate import MailWidgetTemplate

class MyWidget(QMainWindow):
    def __init__(self, openEmailFormCallback, refreshMessagesCallback, openNewMessageFormCallback,
                 logoutCallback):
        super().__init__()
        uic.loadUi('uiTemplates/mainForm/mainForm.ui', self)

        self.openEmailFormCallback = openEmailFormCallback
        self.openNewMessageFormCallback = openNewMessageFormCallback


        self.scrollArea: QScrollArea = self.scrollArea
        self.msgVBoxLayout: QVBoxLayout = self.scrollArea.findChild(QVBoxLayout)

        self.refreshButton.clicked.connect(refreshMessagesCallback)

        self.writeMessageFormButton.clicked.connect(openNewMessageFormCallback)
        self.logoutButton.clicked.connect(logoutCallback)

    def refreshMessages(self, messages):

        for i in reversed(range(self.msgVBoxLayout.count()-1)):
            widget = self.msgVBoxLayout.itemAt(i).widget()
            self.msgVBoxLayout.itemAt(i).widget().setParent(None)
            widget.deleteLater()

        for message in messages:
            self.__addNewEmail(message['sender_login'], message['text'], message['id'])



    def openEmail(self):
        emailId = self.sender().objectName().split('email_')[1]
        self.openEmailFormCallback(emailId)
        # self.viewMail = MailViewFormTemplate("aboba@mail.ru", "Привет!", "obj123")
        # self.viewMail.show()

    def __addNewEmail(self, senderAddress, emailText, emailId):
        newEmail = MailWidgetTemplate(senderAddress, emailText, f'email_{emailId}')
        newEmail.clicked.connect(self.openEmail)
        self.msgVBoxLayout.insertWidget(0, newEmail)

# def except_hook(cls, exception, traceback):
#     sys.__excepthook__(cls, exception, traceback)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     def closeMailViewFormCallback():
#         del app.viewMailForm
#
#     def emailViewFormCallback(emailId):
#
#         app.viewMailForm = MailViewFormTemplate("aboba@mail.ru", "Привет!", "obj123", closeMailViewFormCallback)
#         app.viewMailForm.show()
#
#
#
#
#     ex = MyWidget(emailViewFormCallback)
#
#     ex.addNewEmail("aboba@mail.ru", "Привет!", "obj123")
#
#
#     sys.excepthook = except_hook
#     ex.show()
#     sys.exit(app.exec_())
