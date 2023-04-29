import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
)
from bootstrap import *
from src.gui.window import App_QMainWindow
from src.backends.data_model import QtDM_Dicom, I_DicomNode

main_window_design_file='./src/gui/ui/mainwindow.ui'

class QtApp:
    def __init__(self, *args, **kwargs):
        self._qt_app                = QApplication(list(args))
        self._qt_win                = App_QMainWindow(main_window_design_file)
        self._dicom_data_model      = QtDM_Dicom()

    def onInit(self):
        self._qt_win.setMinimumSize(app_window_min_width, app_window_min_height)
        self._qt_win.setWindowTitle(app_name.decode(system_encoding))
        self._qt_win.centerWinPos()
        self._qt_win.setDataModelToWidget('treeView', self._dicom_data_model)

        self._dicom_data_root       = self._dicom_data_model._root

    def onExec(self):
        self.onInit()
        self._qt_win.show()
        return self._qt_app.exec_()