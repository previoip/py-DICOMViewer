
from enum import Enum, auto
from enum_meta import EnumComparable
from pool import InstancePool


class ConfigType(Enum, metaclass=EnumComparable):
    XML = auto()
    JSON = auto()
    INI = auto()


class ConfigHandler(InstancePool):

    def __init__(self):
        super().__init__()


    def closeAllStream(self):
        self.map(lambda x: x.close())

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

        self.addItem(config_instance)

        return config_instance

if __name__ == '__main__':
    conf_handler = ConfigHandler()

    print(conf_handler.newConfig('foo'))