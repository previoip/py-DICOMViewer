from PyQt5 import (
    QtWidgets,
    uic
)
from PyQt5.QtWidgets import (
    qApp,
    QMainWindow,
    QDesktopWidget,
    QMenuBar,
    QAction,
    QMessageBox,
    QFileDialog,
)
from bootstrap import (
    app_prefetch_license, 
    test_preset_data_root,
)

class App_QMainWindow(QMainWindow):
    def __init__(self, *args, design_file='./src/gui/ui/mainwindow.ui', **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(design_file, self)
        self._initUI()

    def _initUI(self):
        self._initMenuBars()

    def _initMenuBars(self):
        self.actionExit.triggered.connect(self._handler_atExit())
        self.actionAbout.triggered.connect(self._invoke_QMB_about)
        self.actionLicense.triggered.connect(self._invoke_QMB_license)
        self.actionAbout_Qt.triggered.connect(self._invoke_QMB_aboutQt)
        self.actionOpen.triggered.connect(self._invoke_QFD_FileDialogRoot)
        self.actionOpen_Test.triggered.connect(self._invoke_QFD_FileDialogTestPreset)

    def _handler_atExit(self):
        return qApp.quit

    def _invoke_QMB_about(self):
        QMessageBox.about(self, 'About', '')

    def _invoke_QMB_license(self):
        QMessageBox.about(self, 'License', app_prefetch_license)

    def _invoke_QMB_aboutQt(self):
        QMessageBox.aboutQt(self)

    def _invoke_QFD_FileDialogRoot(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()", 
            "",
            "All Files (*);;DICOM Files (*.dcm)", 
            options=options
        )
        if fileName:
            print(fileName)

    def _invoke_QFD_FileDialogTestPreset(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()", 
            test_preset_data_root,
            "All Files (*);;DICOM Files (*.dcm)", 
            options=options
        )
        if fileName:
            print(fileName)


    def centerWinPos(self):
        frame_geom = self.frameGeometry()
        center_pos = QDesktopWidget().availableGeometry().center()
        frame_geom.moveCenter(center_pos)
        self.move(frame_geom.topLeft())
