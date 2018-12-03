from simplecrypt import encrypt, decrypt

try:
    from cryptography.assets import getFilePath
except ImportError:
    from assets import getFilePath

def get_pass(fileName):
    file = open(getFilePath("cryptography/bytes",fileName + ".txt"),"rb")
    for combo in file:
        plainText = decrypt(' ', combo)
    plainText = plainText.decode("utf-8")
    file.close()
    return plainText

def save_pass(passw,fileName):
    password = encrypt(' ', passw)
    file = open(getFilePath("cryptography/bytes",fileName + ".txt"),"wb")
    file.write(password)
    file.close()
