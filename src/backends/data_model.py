from pathlib import Path
from bootstrap import *
import os

import pydicom
from pydicom import dcmread
from pydicom.data import (
    get_testdata_files,
)

from PyQt5 import QtWidgets
from PyQt5.QtCore import (
    QAbstractItemModel
)

class App_QtDM_DicomDir(QAbstractItemModel):
    def __init__(self):
        super().__init__()
        self.reader = dcmread
        self.data = None

    def dcm_read(self, path):
        self.data = dcmread(path)
    