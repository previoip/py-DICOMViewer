from enum import Enum, auto
from uuid import uuid4
from metaclass_enum import EnumComparable
import os

class ConfigType(Enum, metaclass=EnumComparable):
    XML  = auto()
    JSON = auto()
    INI  = auto()

class BaseConfigContainer:
    def __init__(self, _type, _id, path):
        if not os.access(self._path, os.W_OK | os.R_OK):
            raise NameError(f'invalid file mode on config file: {path}')

        self._type  = _type
        self._id    = _id
        self._path  = path
        self._data  = {}
        self._uuid  = uuid4()

    def load(self):
        self._loader()
    
    def _loader(self):
        ...

    def save(self):
        self._unloader()

    def _unloader(self):
        ...


class ConfigHandler:

    def __init__(self):
        self._pool = {}
        self._cfg_uuid = []

    def iterConfigPool(self):
        return iter(self._pool.values())

    def getUUIDs(self):
        return list(map(lambda x: x._uuid, self.iterConfigPool()))

    def getIDs(self):
        return list(map(lambda x: x._id, self.iterConfigPool()))

    def addConfigContainer(self, config):
        if config._uuid in map(lambda x: x._uuid, self.iterConfigPool()):
            return
        self._pool[config._uuid] = config
        self._cfg_uuid.append(config._uuid)

    def newConfig(self, config_type: ConfigType):

        config_instance = None
        if not config_type in ConfigType:
            return None

        elif config_type == ConfigType.INI:
            config_instance = None

        elif config_type == ConfigType.JSON:
            config_instance = None

        elif config_type == ConfigType.XML:
            config_instance = None

        self.addConfigContainer(config_instance)

        return config_instance

if __name__ == '__main__':
    print(os.access('config.xml', os.W_OK | os.R_OK))
