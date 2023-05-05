class Node:
    def __init__(self, parent=None):
        self._parent = parent
        self._children = []
        self.__clear_lock = False
        if parent is not None and isinstance(parent, self.__class__):
            parent.addChild(self) 

    def getParent(self):
        return self._parent

    def getRootNode(self):
        curr = self._parent
        previous = self
        while curr is not None:
            previous = curr
            curr = curr.getParent()
        return previous

    def index(self):
        if isinstance(self._parent, self.__class__) and self._parent is not None:
            return self._parent._children.index(self)
        return 0

    def addChild(self, child):
        self._children.append(child)

    def getChild(self, n):
        return self._children[n]

    def getChildCount(self):
        return len(self._children)

    def clear(self):
        self.__clear_lock = True
        for child in self._children:
            if isinstance(child, self.__class__):
                if not child.__clear_lock:
                    child.clear()
            del child
        self._children.clear()