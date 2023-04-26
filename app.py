import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
)
from bootstrap import *
from src.gui.window import App_QMainWindow

class AppQT:
    def __init__(self, argv):
        self._qt_app                = QApplication(argv)
        self._qt_win                = App_QMainWindow()
        # self._app_config_default    = newConfigFromPath('default', app_fpath_config)
    
    def onInit(self):
        self._qt_win.setMinimumSize(app_window_min_width, app_window_min_height)
        self._qt_win.setWindowTitle(app_name.decode(system_encoding))
        self._qt_win.centerWinPos()

    def onExec(self):
        self.onInit()
        self._qt_win.show()
        return self._qt_app.exec_()