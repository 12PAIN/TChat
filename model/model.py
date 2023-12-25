import sys

from PyQt5.QtCore import QSettings, QCoreApplication
from PyQt5.QtWidgets import QApplication

from exceptions.UserNotCreatedYet import UserNotCreatedYet
from repository.tChatRepository import TChatRepository
from templateModels.emailViewForm.emailViewFormTemplate import MailViewFormTemplate
from viewModels.main.mainForm import MyWidget
from viewModels.signViewModels.signIn.signInForm import SignInForm
from viewModels.signViewModels.signUp.signUpForm import SignUpForm
from viewModels.writeMessageForm.writeMessageForm import WriteMessageForm

ORGANIZATION_NAME = '12Pain'
ORGANIZATION_DOMAIN = '12pain.ru'
APPLICATION_NAME = 'TChat'


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class MainAppModel:

    def __init__(self, repository: TChatRepository | None = None):

        QCoreApplication.setApplicationName(ORGANIZATION_NAME)
        QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
        QCoreApplication.setApplicationName(APPLICATION_NAME)

        settings = QSettings()

        self.id: int | None = settings.value('userId', -1, int)
        self.login: str | None = settings.value('userLogin', None, str)

        self.repository = repository

        self.app = QApplication(sys.argv)

        self.app.mainForm = None

        if self.id == -1:
            self.startLoginForm()
        else:
            self.startMainForm()
            self.refreshMessages()

        self.app.writeMessageForm = None
        self.app.viewMailForm = None

        sys.excepthook = except_hook
        sys.exit(self.app.exec_())

    def startLoginForm(self):
        self.app.loginForm = SignInForm(self.signInCallback, self.openRegisterFormCallback)
        self.app.loginForm.show()

    def logoutCallback(self):
        settings = QSettings()
        settings.clear()

        self.id = None
        self.login = None

        if self.app.mainForm is not None:
            self.app.mainForm.hide()
            del self.app.mainForm

        self.startLoginForm()


    def openRegisterFormCallback(self):
        self.app.loginForm.hide()
        self.app.registerForm = SignUpForm(self.registerUserCallback, self.closeRegisterFormCallback)
        self.app.registerForm.show()

    def signInCallback(self, login, hashedPassword):

        userInfo = self.repository.getUserInfoByLogin(login)
        if userInfo['password'] != hashedPassword:
            return False

        settings = QSettings()

        self.id = userInfo['id']
        self.login = login

        settings.setValue('userId', self.id)
        settings.setValue('userLogin', self.login)

        self.app.loginForm.hide()
        del self.app.loginForm
        self.startMainForm()

    def openWriteMessageForm(self):
        self.app.writeMessageForm = WriteMessageForm(self.sendMessageCallback)
        self.app.writeMessageForm.show()

    def sendMessageCallback(self, receiverLogin, messageText, imageData, imageExtension):

        try:
            if imageData is None:
                self.repository.addMessage(int(self.id), receiverLogin, messageText)
            else:
                self.repository.addMessage(int(self.id), receiverLogin, messageText, imageData, imageExtension)

            self.app.writeMessageForm.hide()
            del self.app.writeMessageForm
        except UserNotCreatedYet as e:
            return False

    def registerUserCallback(self, login, hashedPassword):

        try:
            self.repository.addUser(login, hashedPassword)
        except Exception as e:
            return False

        self.closeRegisterFormCallback()

    def closeRegisterFormCallback(self):
        self.app.registerForm.hide()
        del self.app.registerForm

        self.app.loginForm.show()

    def startMainForm(self):
        mainForm = MyWidget(self.emailViewFormCallback, self.refreshMessagesCallback,
                            self.openWriteMessageForm, self.logoutCallback)
        mainForm.show()
        self.app.mainForm = mainForm
        self.refreshMessages()

    def refreshMessagesCallback(self):
        self.refreshMessages()

    def refreshMessages(self):

        messages = self.repository.getAllMessagesByUserLogin(self.login)
        self.app.mainForm.refreshMessages(messages)

    def closeMailViewFormCallback(self):
        del self.app.viewMailForm

    def emailViewFormCallback(self, emailId):

        message = self.repository.getMessageById(int(emailId))

        self.app.viewMailForm = MailViewFormTemplate(message['sender_login'], message['text'],
                                                     emailId, self.closeMailViewFormCallback,
                                                     message['image'], message['image_extension'])
        self.app.viewMailForm.show()
