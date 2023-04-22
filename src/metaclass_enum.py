from enum import EnumMeta

class EnumComparable(EnumMeta):
    def __contains__(cls, item): 
        return isinstance(item, cls) or item in [v.value for v in cls.__members__.values()] 
