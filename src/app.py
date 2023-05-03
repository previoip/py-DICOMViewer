import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
)
from bootstrap import *
from src.window import App_QMainWindow
from src.data_model import QtDataModelDicomPatientRecord, parseDicomFromPath

main_window_design_file='./src/ui/mainwindow.ui'

class QtApp:
    def __init__(self, *args, **kwargs):
        self._qt_app                = QApplication(list(args))
        self._qt_win                = App_QMainWindow(main_window_design_file)
        self._dicom_data_model      = QtDataModelDicomPatientRecord()

    def onInit(self):
        self._qt_win.setWindowTitle(
            app_name.decode(system_encoding) + " - " + \
            app_version.decode(system_encoding)
            )
        self._qt_win.setDataModelToWidget('treeView', self._dicom_data_model)

    def postInit(self):
        self._dicom_data_root       = self._dicom_data_model.getParentNode().getRootNode()
        self._qt_win._active_path   = os.path.join(test_preset_data_path, 'dicomdirtests', 'DICOMDIR')
        parseDicomFromPath(self._qt_win._active_path, self._dicom_data_root)
        self._qt_win.postInit()

    def onExec(self):
        self.onInit()
        self._qt_win.show()
        self.postInit()
        return self._qt_app.exec_()