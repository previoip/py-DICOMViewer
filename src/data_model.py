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
    Qt,
)

from src.node import Node



class IDicomPatientRecordNode(Node):
    def __init__(self, display_name, obj_weakref=None, parent=None):
        super().__init__(parent)
        self.display_name = display_name
        self.active = False
        self._obj_weakref = obj_weakref
        self._obj_weakref_access = False

    def setObjWeakReference(self, obj_weakref):
        self._obj_weakref = obj_weakref

    def isObjAccessible(self):
        return self._obj_weakref_access
    
    def setObjAccess(self, b):
        self._obj_weakref_access = b

    def getObj(self):
        return self._obj_weakref

class QtDataModelDicomPatientRecord(QAbstractItemModel):
    def __init__(self, dicom_node=IDicomPatientRecordNode('root')):
        super().__init__()
        self._node = dicom_node

    def getNode(self):
        return self._node

    def replaceNode(self, root_node):
        self._node.clear()
        self._node = root_node


    # QAbstractItemModel class method overrides

    def parent(self, index):
        dicom_node = index.internalPointer()
        if not isinstance(dicom_node, IDicomPatientRecordNode):
            return QModelIndex()
        parent_node = dicom_node.getParent()
        if parent_node == self._node:
            return QModelIndex()
        return self.createIndex(parent_node.index(), 0, parent_node)

    def rowCount(self, index):
        if index.isValid():
            parent_node = index.internalPointer()
        else:
            parent_node = self._node
        return parent_node.getChildCount()

    def index(self, row, column, parent):
        if parent.isValid():
            parent_node = parent.internalPointer()
        else:
            parent_node = self._node
        child = parent_node.getChild(row)

        if child and child is not None:
            return self.createIndex(row, column, child)
        return QModelIndex()

    def columnCount(self, index):
        return 1

    def flags(self, index):
        flags = QAbstractItemModel.flags(self, index)
        return flags

    def data(self, index, role):
        if not index.isValid():
            return None
        dicom_node = index.internalPointer()
        row = index.row()
        status = '[x]' if dicom_node.active else '[ ]'
        if role == Qt.DisplayRole:
            return f'{status} {row + 1}. {dicom_node.display_name}'


def parseDicomFromPath(path, dicom_node=IDicomPatientRecordNode('root')):

    def __recurse(ds, root):
        if not isinstance(ds, Dataset):
            return
        if not hasattr(ds, 'DirectoryRecordType'):
            return

        dirtype = ds.DirectoryRecordType
        trunk = IDicomPatientRecordNode(dirtype, ds, root)

        if dirtype in ['IMAGE']:
            trunk.display_name = f'<{trunk.display_name}>'
            trunk.setObjAccess(True)

        if hasattr(ds, 'children'):
            for child in ds.children:
                __recurse(child, trunk)

    dicom_node.clear()
    ds = dcmread(path)
    ds.ensure_file_meta()
    main_trunk = IDicomPatientRecordNode(os.path.basename(path), ds, dicom_node)

    if hasattr(ds, 'patient_records'):
        for record in ds.patient_records:
            __recurse(record, main_trunk)

    if hasattr(ds, 'pixel_array'):
        main_trunk.setObjAccess(True)

    return dicom_node
