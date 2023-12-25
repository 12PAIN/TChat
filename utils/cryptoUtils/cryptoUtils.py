import hashlib

def getMd5HashOfString(inputStr: str):
    return hashlib.md5(inputStr.encode('utf-8')).hexdigest()


