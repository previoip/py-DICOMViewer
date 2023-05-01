from PyQt5 import (
    QtWidgets,
    uic
)
from PyQt5.QtWidgets import (
    qApp,
    QMainWindow,
    QWidget,
    QDesktopWidget,
    QMenuBar,
    QAction,
    QMessageBox,
    QFileDialog,
    QDirModel,
    QTableWidgetItem,
    QHeaderView,
)

from PyQt5.QtCore import (
    pyqtSignal,
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

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

import os
from pathlib import Path

class MplCanvas(FigureCanvas):
    def __init__(self, parent):
        self.fig, self.ax = plt.subplots(dpi=72, layout="constrained")
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax.margins(0)


class App_QMainWindow(QMainWindow):

    resize_signal = pyqtSignal()

    def __init__(self, design_file='./src/gui/ui/mainwindow.ui'):
        super().__init__()
        uic.loadUi(design_file, self)
        self._initUI()
        self._active_model = {}
        self._active_path = ''
    
    def postInit(self):
        self.resize_signal.emit()

    def setDataModelToWidget(self, widget_selector, model):
        widget = getattr(self, widget_selector)
        if not isinstance(widget, QWidget):
            raise NameError(f'widget_selector does not point to active widget {widget_selector}')
        widget.setModel(model)
        self._active_model[widget_selector] = model

    def resizeEvent(self, event):
        self.resize_signal.emit()
    
    def _initUI(self):
        self._initMenuBars()
        self._initTreeViewWidget()
        self._initTableWidget()
        self._initMplCanvas()

    def _initMenuBars(self):
        self.actionExit.triggered.connect(self._handler_atExit())
        self.actionAbout.triggered.connect(self._invoke_QMB_about)
        self.actionLicense.triggered.connect(self._invoke_QMB_license)
        self.actionAbout_Qt.triggered.connect(self._invoke_QMB_aboutQt)
        self.actionOpen.triggered.connect(self._invoke_QFD_FileDialogRoot)
        self.actionOpen_Test.triggered.connect(self._invoke_QFD_FileDialogTestPreset)

    def _initTreeViewWidget(self):
        self.treeView.clicked.connect(self._handler_treeView_updateOnItemSelect)
        self.treeView.clicked.connect(self._handler_loadImageToCanvas)

    def _initTableWidget(self):
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def _initMplCanvas(self):
        self.MplWidget = self.frame
        self.MplChart = MplCanvas(self.MplWidget)
        self.resize_signal.connect(self._handler_MplCanvas_onResize)

    def _handler_MplCanvas_onResize(self):
        parent_frame_geom = self.MplWidget.frameGeometry()
        self.MplChart.setGeometry(parent_frame_geom)

    def _handler_treeView_updateOnItemSelect(self, index):
        table_widget = self.tableWidget
        dicom_node = index.internalPointer()

        row = table_widget.rowCount()
        for i in range(row):
            table_widget.removeRow(i)

        ds = dicom_node._obj_ref
        els = [i for i in ds]
        table_widget.setRowCount(len(els))

        for r, el in enumerate(els):
            table_widget.setItem(r, 0, QTableWidgetItem(el.name))
            table_widget.setItem(r, 1, QTableWidgetItem(el.repval))

    def _handler_loadImageToCanvas(self, index):
        canvas_widget = self.MplChart

        dicom_node = index.internalPointer()

        if not dicom_node._obj_ref_access:
                return

        root_dicom_node = dicom_node.getRootNode().getChild(0)
        root_dicom_path = Path(root_dicom_node._obj_ref.filename)
        ds = dicom_node._obj_ref
        
        ds_img = None
        if 'ReferencedFileID' in ds:
            el = ds['ReferencedFileID']
            if el.VM == 1:
                relpath_to_img = el.value
            elif el.VM > 1:
                relpath_to_img = os.path.join(*el.value)
            
            relpath_to_img = Path(self._active_path).parent / Path(relpath_to_img)
            ds_img = dcmread(relpath_to_img.resolve())

        elif hasattr(ds, 'pixel_array'):
            relpath_to_img = root_dicom_path
            ds_img = ds

        if ds_img is None:
            return

        canvas_widget.ax.imshow(ds_img.pixel_array, cmap=plt.cm.gray)
        canvas_widget.draw()
        


    def _handler_atExit(self):
        return qApp.quit

    def _handler_dicomFileOpen(self, file_path):
        self._active_path = file_path
        root = IDicomPatientRecordNode('root')
        self._active_model['treeView'].replaceNode(root)
        parseDicomFromPath(file_path, root)
        self._active_model['treeView'].layoutChanged.emit()

    def _wrapper_invoke_QFileDialog(self, path, _filter = "All Files (*)"):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        def wrapper(*args, **kwargs):
            return QFileDialog.getOpenFileName(
            self,
            "Open File", 
            path,
            _filter, 
            options=options
        )
        return wrapper

    def _invoke_QMB_about(self):
        QMessageBox.about(self, 'About', '')

    def _invoke_QMB_license(self):
        QMessageBox.about(self, 'License', app_prefetch_license)

    def _invoke_QMB_aboutQt(self):
        QMessageBox.aboutQt(self)

    def _invoke_QFD_FileDialogRoot(self):
        file_path, _ = self._wrapper_invoke_QFileDialog(
            "",
            "All Files (*);;DICOM Files (*.dcm)" 
            )()
        if file_path:
            self._handler_dicomFileOpen(file_path)

    def _invoke_QFD_FileDialogTestPreset(self):
        file_path, _ = self._wrapper_invoke_QFileDialog(
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
