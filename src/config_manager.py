from enum import Enum, auto
import os
import sys
from json import (
    dumps as json_dumps,
    load as json_load
)
from xml.etree import ElementTree as xml_et

from src.metaclass_enum import EnumComparable
from src.file_util import raiseFileMode, createFileIfNotExist, ensureExtension, checkFileExtension
from src.hash_util import sha1_digest



# config pool for batch processes
_config_pool = []

class ConfigType(Enum, metaclass=EnumComparable):
    XML  = auto()
    JSON = auto()
    INI  = auto()

class _BaseConfigContainer:

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
        self.uid        = _BaseConfigContainer.id_to_uid(self.id)

    def load(self):
        self._loader()

    def save(self):
        with open(self.filepath, 'wb') as fo:
            fo.write(self._unloader())

    def _loader(self):
        raise NotImplementedError('loader is not yet implemented/overridden')

    def _unloader(self) -> bytes:
        raise NotImplementedError('unloader is not yet implemented/overridden')


class ConfigContainerXML(_BaseConfigContainer):
    def __init__(self, _id, filepath):
        filepath = ensureExtension(filepath, 'xml')
        super().__init__(ConfigType.XML, _id,  filepath)

    def _loader(self):
        self.data = xml_et.parse(self.filepath)

    def _unloader(self) -> bytes:
        return bytes(xml_et.tostring(self.data), encoding='us-ascii')

class ConfigContainerJSON(_BaseConfigContainer):
    def __init__(self, _id, filepath):
        filepath = ensureExtension(filepath, 'json')
        super().__init__(ConfigType.JSON, _id,  filepath)

    def _loader(self):
        self.data = json_load(self.filepath)

    def _unloader(self) -> bytes:
        return bytes(json_dumps(self.data), encoding='utf-8')

class ConfigContainerINI(_BaseConfigContainer):
    def __init__(self, _id, filepath):
        filepath = ensureExtension(filepath, 'ini')
        super().__init__(ConfigType.INI, _id,  filepath)

    # def _loader(self):
    #     ...

    # def _unloader(self) -> bytes:
    #     ...

def getConfigPoolIds():
    return list(map(lambda x: x.id, _config_pool))

def getConfigById(_id):
    return _config_pool[getConfigPoolIds().index(_id)]

def isConfigExistById(_id):
    return _id in map(lambda x: x.id, _config_pool)

def newConfig(_type: ConfigType, _id: str, filepath):
    if _type not in ConfigType:
        raise NotImplementedError('Container is not yet implemented/overridden')
    elif isConfigExistById(_id):
        # raise NameError(f'Container id already exist: {_id}')
        return getConfigById(_id)
    elif _type == ConfigType.XML:
        c = ConfigContainerXML(_id, filepath)
    elif _type == ConfigType.JSON:
        c = ConfigContainerJSON(_id, filepath)
    elif _type == ConfigType.INI:
        c = ConfigContainerINI(_id, filepath)
    else:
        raise NameError('Could not create config file')
    _config_pool.append(c)
    return c

def newConfigFromPath(_id: str, filepath):
    if checkFileExtension(filepath, 'xml'):
        return newConfig(ConfigType.XML, _id, filepath)
    elif checkFileExtension(filepath, 'json'):
        return newConfig(ConfigType.JSON, _id, filepath)
    elif checkFileExtension(filepath, 'ini'):
        return newConfig(ConfigType.INI, _id, filepath)
    else:
        raise NotImplementedError('config container for file is not yet implemented')

def removeConfigFile(_id):
    return _config_pool.pop(getConfigPoolIds().index(_id))

def loadAllConfig():
    for confc in _config_pool:
        confx.load()

def saveAllConfig():
    for confc in _config_pool:
        confx.save()


def flushConfigPool():
    c = _config_pool.copy()
    _config_pool.clear()
    return c