from enum import Enum, auto
from hashlib import sha1
import os
import sys
from src.metaclass_enum import EnumComparable
from src.file_util import raiseFileMode, createFileIfNotExist
from src.hash_util import sha1_to_hex

config_pool = []

class ConfigType(Enum, metaclass=EnumComparable):
    XML  = auto()
    JSON = auto()
    INI  = auto()

class BaseConfigContainer:

    @staticmethod
    def id_to_uid(string_id):
        return sha1_digest(
            bytes(
                string_id,
                encoding=sys.getfilesystemencoding()
            )
        )


    def __init__(self, _type, _id, filepath):
        createFileIfNotExist(filepath)
        raiseFileMode(filepath)
        self.id         = _id
        self._type      = _type
        self.filepath   = filepath
        self.data       = None
        self.uid        = BaseConfigContainer.id_to_uid(self.id)

    def load(self):
        self._loader()

    def save(self):
        with open(self.filepath, 'wb') as fo:
            fo.write(self._unloader())

    def _loader(self):
        raise NotImplementedError('loader is not yet implemented')

    def _unloader(self) -> bytes:
        raise NotImplementedError('unloader is not yet implemented')


class ConfigContainerXML(BaseConfigContainer):
    def __init__(self, _id, filepath):
        super().__init__(ConfigType.XML, _id,  filepath)

    def _loader(self):
        ...

    def _unloader(self) -> bytes:
        ...

class ConfigContainerJSON(BaseConfigContainer):
    def __init__(self, _id, filepath):
        super().__init__(ConfigType.JSON, _id,  filepath)

    def _loader(self):
        ...

    def _unloader(self) -> bytes:
        ...

class ConfigContainerINI(BaseConfigContainer):
    def __init__(self, _id, filepath):
        super().__init__(ConfigType.INI, _id,  filepath)

    def _loader(self):
        ...

    def _unloader(self) -> bytes:
        ...

def isConfigExistById(_id):
    return _id in map(lambda x: x.id, config_pool)

def newConfig(_type: ConfigType, _id: str, filepath):
    if _type not in ConfigType:
        raise NotImplementedError('Container is not yet implemented')

    elif isConfigExistById(_id):
        raise NameError(f'Container id already exist: {_id}')
    elif _type == ConfigType.XML:
        c = ConfigContainerXML(_id, filepath)
    elif _type == ConfigType.JSON:
        c = ConfigContainerJSON(_id, filepath)
    elif _type == ConfigType.INI:
        c = ConfigContainerINI(_id, filepath)
    else:
        raise NameError('Could not create config file')

    config_pool.append(c)

    return c