from pathlib import Path
from bootstrap import *
import os

from pydicom.dataset import (
    Dataset,
    FileDataset,
    DataElement,
)
from pydicom.multival import MultiValue
from pydicom.sequence import Sequence

from PyQt5 import QtWidgets
from PyQt5.QtCore import (
    QAbstractItemModel,
    QModelIndex,
    Qt
)



class I_DicomNode:
    def __init__(self, name, ref=None, parent=None):
        self.name = name

        self._ref = ref
        self._children = []
        self._parent = parent

        if isinstance(parent, self.__class__) and parent is not None:
            parent.addChild(self)

    def parent(self):
        return self._parent

    def index(self):
        if isinstance(self._parent, self.__class__) and self._parent is not None:
            return self._parent._children.index(self)
        return -1

    def addChild(self, child):
        self._children.append(child)

    def getChild(self, n):
        return self._children[n]

    def getChildCount(self):
        return len(self._children)

    def clear(self):
        for child in self._children:
            if isinstance(child, self.__class__):
                child.clear()
            del child
        self._children.clear()

class QtDM_Dicom(QAbstractItemModel):
    def __init__(self, dicom_node=I_DicomNode('Empty'), parent=None):
        super().__init__()
        self._root = dicom_node

    def parent(self, index):
        dicom_node = index.internalPointer()
        parent_node = dicom_node.parent()

        if parent_node == self._root:
            return QModelIndex()
        return self.createIndex(parent_node.index(), 0, parent_node)

    def rowCount(self, index):
        if index.isValid():
            parent_node = index.internalPointer()
        else:
            parent_node = self._root
        return parent_node.getChildCount()

    def index(self, row, column, parent):
        if not parent.isValid():
            parent_node = self._root
        else:
            parent_node = parent.internalPointer()
        child = parent_node.getChild(row)
        
        if child and child is not None:
            return self.createIndex(row, column, child)
        return QModelIndex()

    def columnCount(self, index):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None
        dicom_node = index.internalPointer()
        if role == Qt.DisplayRole:
            return dicom_node.name


def parseDicomDataset(ds, parent=I_DicomNode('root')):
    for elem in ds:
        node = I_DicomNode(f'{elem.VR}, {elem.value}', elem, parent)
        if isinstance(elem, Dataset):
            parseDicomDataset(elem, node)
        elif isinstance(elem, Sequence):
            parseDicomDataset(seq, node)
