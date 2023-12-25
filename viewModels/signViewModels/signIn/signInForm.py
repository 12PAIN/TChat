from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMainWindow
from utils.cryptoUtils.cryptoUtils import getMd5HashOfString

class SignInForm(QMainWindow):

    def __init__(self, signInCallback, openRegisterFormCallback):
        super().__init__()
        self.signInCallback = signInCallback

        uic.loadUi('uiTemplates/loginForm/loginForm.ui', self)
        self.signInPushButton.clicked.connect(self.handleSignIn)
        self.signUpPushButton.clicked.connect(openRegisterFormCallback)

    def handleSignIn(self):

        login = self.loginInput.text()
        hashedPassword = getMd5HashOfString(self.passwordInput.text())

        result: bool = self.signInCallback(login, hashedPassword)

        if not result:
            self.statusBar.showMessage(f'Ошибка! Вход не выполнен!')


