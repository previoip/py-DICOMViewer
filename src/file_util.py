import os

def raiseFileMode(path, mode_flag=os.W_OK | os.R_OK):
    if not os.access(path, mode_flag):
        raise PermissionError(f'invalid file mode on file: {path}')

def createFileIfNotExist(path):
    if not os.path.exists(path):
        open(path, 'x').close()
