from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    qApp,
    QMainWindow,
    QDesktopWidget,
    QMenuBar,
    QAction,
    QMessageBox,
)

class App_QMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initUI()

    def _initUI(self):

        act_exit = QAction('&Exit', self)
        act_exit.setShortcut('Ctrl+Q')
        act_exit.setStatusTip('Exit application')
        act_exit.triggered.connect(qApp.quit)

        act_about = QAction('&About', self)
        act_about.triggered.connect(self.about)

        self.statusBar()

        menubar = self.menuBar()
        menu_file = menubar.addMenu('&File')
        menu_file.addAction(act_exit)
        menu_about = menubar.addMenu('&About')
        menu_about.addAction(act_about)

    def about(self):
        QMessageBox.about(self, 'About', '')

    def centerWinPos(self):
        frame_geom = self.frameGeometry()
        center_pos = QDesktopWidget().availableGeometry().center()
        frame_geom.moveCenter(center_pos)
        self.move(frame_geom.topLeft())
