from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow

from exceptions import passwordExceptions
from utils.cryptoUtils.cryptoUtils import getMd5HashOfString
import utils.passwordCheckUtil as passwordChecker


class SignUpForm(QMainWindow):
    closing = pyqtSignal()

    def closeEvent(self, event: QCloseEvent):
        self.closeCallback()
        self.closing.emit()

    def __init__(self, registerUserCallback, closeCallback):
        super().__init__()
        self.registerUserCallback = registerUserCallback
        self.closeCallback = closeCallback

        uic.loadUi('uiTemplates/registerForm/registerForm.ui', self)
        self.signUpPushButton.clicked.connect(self.handleRegistration)

    def handleRegistration(self):

        login = self.loginInput.text()

        if len(login) < 5:
            self.statusBar.showMessage(f'Ошибка! Длина логина меньше 5 символов!')
            return


        try:
            password = self.passwordInput.text()

            passwordChecker.checkPassword(password)

            self.statusBar.showMessage(f'Успех! Вы зарегистрированы!')
        except passwordExceptions.LetterError:
            self.statusBar.showMessage(f'Ошибка! Ваш пароль не содержит больших или маленьких букв!')
            return
        except passwordExceptions.DigitError:
            self.statusBar.showMessage(f'Ошибка! Ваш пароль не содержит цифр!')
            return
        except passwordExceptions.LengthError:
            self.statusBar.showMessage(f'Ошибка! Длина пароля меньше 8 символов!')
            return
        except passwordExceptions.SequenceError:
            self.statusBar.showMessage(f'Ошибка! Ваш пароль содержит последовательности!')
            return


        hashedPassword = getMd5HashOfString(password)

        if not self.registerUserCallback(login, hashedPassword):
            self.statusBar.showMessage(f'Ошибка! Такой пользователь уже существует!')
            return
