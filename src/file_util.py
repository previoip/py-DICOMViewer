import os
from dataclasses import dataclass

def raiseFileMode(path, mode_flag=os.W_OK | os.R_OK):
    if not os.access(path, mode_flag):
        raise PermissionError(f'invalid file mode on file: {path}')

def createFileIfNotExist(path):
    if not os.path.exists(path):
        open(path, 'x').close()

def raiseIsFile(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError('file not found')
    if not os.path.isfile(filepath):
        raise NameError(f'target path is not a file: {filepath}')

def checkFileExtension(filepath, ext):
    return str(filepath).split('.')[-1].casefold().lower() == ext.casefold().lower()

def ensureExtension(filepath, ext):
    path_tail, path_extension = filepath.split('.')
    if not checkFileExtension(filepath, ext):
        filepath = f'{path_tail}.{ext}'
    return filepath
