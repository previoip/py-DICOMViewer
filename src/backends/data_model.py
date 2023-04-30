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


class IDicomPatientRecordNode:
    def __init__(self, name, obj_ref=None, parent=None):
        self.name = name
        self.obj_ref = obj_ref
        self._parent = parent
        self._children = []
        self.__clear_lock = False

        if isinstance(parent, self.__class__) and parent is not None:
            parent.addChild(self)

    def getParent(self):
        return self._parent

    def getRootNode(self):
        curr = self._parent
        previous = None
        while curr is not None:
            previous = curr
            curr = curr.getParent()
        return previous

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
        self.__clear_lock = True
        for child in self._children:
            if isinstance(child, self.__class__):
                if not child.__clear_lock:
                    child.clear()
        self._children.clear()
        self.__clear_lock = False



class QtDataModelDicomPatientRecord(QAbstractItemModel):
    def __init__(self, dicom_node=IDicomPatientRecordNode('root')):
        super().__init__()
        self._node = dicom_node

    def getParentNode(self):
        return self._node

    def parent(self, index):
        dicom_node = index.internalPointer()
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
        if not parent.isValid():
            parent_node = self._node
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


def parseDicomFromPath(path, dicom_node=IDicomPatientRecordNode('root')):
    # assumes Dataset or Dircom/FileDataset is flat
    dicom_node.clear()
    ds = dcmread(path)

    ds.ensure_file_meta()
    main_trunk = IDicomPatientRecordNode(os.path.basename(path), ds, dicom_node)

    def filterPredicateDirType(dir_type_selector, value):
        return lambda x: getattr(x, dir_type_selector) == value

    if hasattr(ds, 'patient_records'):
        for record in ds.patient_records:
            patient_id = record.PatientID
            patient_name = record.PatientName

            record_trunk = IDicomPatientRecordNode(patient_name, None, main_trunk)

            for study in record.children:
                if study.DirectoryRecordType != 'STUDY':
                    continue

                study_id = study.StudyID
                study_date = study.StudyDate
                study_desc = getattr(study, 'StudyDescription', 'undefined')

                study_trunk = IDicomPatientRecordNode(study_id, None, record_trunk)

                for series in study.children:
                    if series.DirectoryRecordType != 'SERIES':
                        continue

                    series_desc = getattr(series, 'SeriesDescription', 'undefined')
                    series_number = getattr(series, 'SeriesNumber', 'undefined')

                    series_trunk = IDicomPatientRecordNode(series_number, None, study_trunk)

                    for image in series.children:
                        if image.DirectoryRecordType != 'IMAGE':
                            continue

        # name = fetchFilesetIdRepr(ds)
        # for elem in ds:
        #     if elem.VR == 'SQ':
        #         [recurse(item, trunk) for item in elem.value]

    return dicom_node

def fetchFilesetIdRepr(ds):
    assert isinstance(ds, FileDataset)
    if 'PatientName' in ds:
        return ds.get('PatientName')
    elif 'PatientID' in ds:
        return ds.get('PatientName')
    return 'undefined'
