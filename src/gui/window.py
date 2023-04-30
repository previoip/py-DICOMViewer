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
    QDirModel
)

from bootstrap import (
    app_prefetch_license, 
    test_preset_data_path,
)
from src.backends.data_model import (
    QtDataModelDicomPatientRecord,
    IDicomPatientRecordNode,
    parseDicomFromPath
)

from pydicom import (
    dcmread,
)

class App_QMainWindow(QMainWindow):
    def __init__(self, design_file='./src/gui/ui/mainwindow.ui'):
        super().__init__()
        uic.loadUi(design_file, self)
        self._initUI()
        self._active_model = {}

    def setDataModelToWidget(self, widget_selector, model):
        getattr(self, widget_selector).setModel(model)
        self._active_model[widget_selector] = model


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

    def _handler_dicomFileOpen(self, file_path):
        root = IDicomPatientRecordNode('root')
        self._active_model['treeView'].replaceNode(root)
        parseDicomFromPath(file_path, root)
        self._active_model['treeView'].layoutChanged.emit()

    def _constructor_invoke_QFileDialog(self, path, _filter = "All Files (*)"):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        def f(*args, **kwargs):
            return QFileDialog.getOpenFileName(
            self,
            "Open File", 
            path,
            _filter, 
            options=options
        )
        return f

    def _invoke_QMB_about(self):
        QMessageBox.about(self, 'About', '')

    def _invoke_QMB_license(self):
        QMessageBox.about(self, 'License', app_prefetch_license)

    def _invoke_QMB_aboutQt(self):
        QMessageBox.aboutQt(self)

    def _invoke_QFD_FileDialogRoot(self):
        file_path, _ = self._constructor_invoke_fileDialog(
            "",
            "All Files (*);;DICOM Files (*.dcm)" 
            )()
        if file_path:
            self._handler_dicomFileOpen(file_path)

    def _invoke_QFD_FileDialogTestPreset(self):
        file_path, _ = self._constructor_invoke_fileDialog(
            test_preset_data_path,
            "All Files (*);;DICOM Files (*.dcm)" 
            )()
        if file_path:
            self._handler_dicomFileOpen(file_path)

    def centerWinPos(self):
        frame_geom = self.frameGeometry()
        center_pos = QDesktopWidget().availableGeometry().center()
        frame_geom.moveCenter(center_pos)
        self.move(frame_geom.topLeft())
