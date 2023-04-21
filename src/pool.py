class Pool:
    def __init__(self):
        self._pool = []

    def map(self, fn):
        for proc in self._pool:
            fn(proc)

    def addItem(self, item):
        self._pool.append(item)

    def getAllItem(self):
        return self._pool


class InstancePool(Pool):
    def __init__(self):
        super().__init__()