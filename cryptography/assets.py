import os

def getFilePath(folder,fileName):
    path = os.getcwd()
    if folder in path:
        path = os.getcwd() + "/" + fileName
    else:
        path = os.getcwd() + "/" + folder + "/" + fileName
    return path
