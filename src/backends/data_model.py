from pathlib import Path
from bootstrap import *
import os

from pydicom import dcmread
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

    def getParent(self):
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
        self._children.clear()





class QtDM_Dicom(QAbstractItemModel):
    def __init__(self, dicom_node=I_DicomNode('root')):
        super().__init__()
        self._root = dicom_node

    def getRootNode(self):
        return self._root

    def parent(self, index):
        dicom_node = index.internalPointer()
        parent_node = dicom_node.getParent()

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


def parseDicomFromPath(path, dicom_node=I_DicomNode('root')):
    dicom_node.clear()
    ds = dcmread(path)

    def recurse(ds, parent):
        ds.ensure_file_meta()
        name = fetchDatasetRepr(ds)
        trunk = I_DicomNode(name, ds, parent)
        for elem in ds:
            if elem.VR == 'SQ':
                [recurse(item, trunk) for item in elem.value]
            else:
                pass

    recurse(ds, dicom_node)

def fetchDatasetRepr(ds):
    if hasattr(ds, 'filename'):
        return os.path.basename(ds.filename)
    file_meta = ds.file_meta
    media_storage_class_sop_uid = file_meta.get('MediaStorageSOPClassUID', None)
    if media_storage_class_sop_uid is not None:
        return media_storage_class_sop_uid.name

    if hasattr(ds, 'PatientID'):
        return 'PatientID: ' + ds.PatientID

    return 'undefined'
