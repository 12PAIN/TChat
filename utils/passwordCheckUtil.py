import exceptions.passwordExceptions as passwordExceptions

lang = ['йцукенгшщзхъ', 'фывапролджэё', 'ячсмитьбю', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm', '1234567890']
nums = set('1234567890')
sla = set('йцукенгшщзхъфывапролджэячсмитьбюqwertyuiopasdfghjklzxcvbnm')
sua = set('ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮQWERTYUIOPASDFGHJKLZXCVBNM')


def checkPassword(password):
    if len(password) < 8: raise passwordExceptions.LengthError

    passwd_set = set(password)

    if len(passwd_set & sua) == 0: raise passwordExceptions.LetterError
    if len(passwd_set & sla) == 0: raise passwordExceptions.LetterError
    if len(passwd_set & nums) == 0: raise passwordExceptions.DigitError

    for charIdx in range(len(password) - 2):
        charSeq = password[charIdx:charIdx + 3].lower()
        for keyboardSeq in lang:
            if charSeq in keyboardSeq:
                raise passwordExceptions.SequenceError

    return 'ok'
