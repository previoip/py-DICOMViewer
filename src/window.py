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
    Qt,
    QSize,
    pyqtSignal,
)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)

# HEY
# you might read this and asks yourself what?
# I've found a method to exclude toolitem for
# matplotlib navigation toolbar derived from
# qt5agg backend. Just in case you might be 
# wondering why, usually canvas object have 
#      remove_toolitem()
# bound method to remove toolbar item which 
# is missing in the backend implementation.

# but by looking at the source code, the items
# is a class attribute on its own and thus
# removing it is as straightforward as follows.

__ti = NavigationToolbar.toolitems # or NavigationToolbar2QT.toolitems
__ti.pop(
    __ti.index(
        next(filter(
            lambda a: 'configure_subplots' in a,
            __ti 
        ))
    )
)

# what the above just do uis to remove
# 'configure_subplots' button, which in this
# app, this toolbar always raises UserWarning
# compat with tight_layout, which I find jarring

# you can check it at the following git 
# https://github.com/matplotlib/matplotlib/blob/main/lib/matplotlib/backends/backend_qt.py#L624

from bootstrap import (
    app_prefetch_license, 
    test_preset_data_path,
)

from src.data_model import (
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
        self.fig, self.ax = plt.subplots(
            dpi=72,
            layout="constrained"
        )
        super().__init__(self.fig)
        self.__pixel_arr = []
        self.__axImg = None
        self.setParent(parent)
        self.ax.margins(0)
        self.ax.set_aspect('auto', 'datalim')
        self.cmap = plt.cm.gray

    def resizeFitToParentWidget(self):
        parent_frame_geom = self.parent().frameGeometry()
        self.setGeometry(parent_frame_geom)

    def updateImage(self):
        if self.__axImg is not None:
            self.cmap = self.__axImg.get_cmap()
        if self.__pixel_arr is None or len(self.__pixel_arr) == 0:
            return
        self.ax.cla()
        self.__axImg = self.ax.imshow(self.__pixel_arr, cmap=self.cmap)
        self.draw()

    def setArr(self, pixel_arr):
        self.__pixel_arr = pixel_arr


class App_QMainWindow(QMainWindow):

    resize_signal = pyqtSignal()
    render_signal = pyqtSignal()

    def __init__(self, design_file='./mainwindow.ui'):
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
        self.actionExit.triggered.connect(self._wrapperAtExit())
        self.actionAbout.triggered.connect(self._invokeMessageBoxAbout)
        self.actionLicense.triggered.connect(self._invokeMessageBoxLicense)
        self.actionAbout_Qt.triggered.connect(self._invokeMessageBoxAboutQt)
        self.actionOpen.triggered.connect(self._invokeMessageBoxAtRoot)
        self.actionOpen_Test.triggered.connect(self._invokeFileDialogAtTest)

    def _initTreeViewWidget(self):
        self.treeView.clicked.connect(self._handleOnItemSelect)
        self.treeView.clicked.connect(self._handleLoadDicomData)

    def _initTableWidget(self):
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def _initMplCanvas(self):
        self.MplWidget = self.frame
        self.MplToolbarFrame = self.toolbarFrame
        self.MplCanvas = MplCanvas(self.MplWidget)
        self.MplToolbar = NavigationToolbar(self.MplCanvas, self.MplToolbarFrame)
        self.resize_signal.connect(self._invokeOnResizeEvent)
        self.render_signal.connect(self.invokeImageUpdate)
        self.MplToolbar.setOrientation(Qt.Vertical)

    def _invokeOnResizeEvent(self):
        self.MplCanvas.resizeFitToParentWidget()

    def _handleOnItemSelect(self, index):
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

    def _handleLoadDicomData(self, index):
        canvas_widget = self.MplCanvas

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

        canvas_widget.setArr(ds_img.pixel_array)
        self.render_signal.emit()

    def invokeImageUpdate(self):
        self.MplCanvas.updateImage()

    def _wrapperAtExit(self):
        return qApp.quit

    def _wrapperFileDialog(self, path, _filter = "All Files (*)"):
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

    def _handleAtFileOpen(self, file_path):
        self.treeView.setUpdatesEnabled(False)

        model = self._active_model['treeView']
        root = model.getNode().getRootNode()
        self.setDataModelToWidget('treeView', None)

        self._active_path = file_path
        parseDicomFromPath(file_path, root)

        self.setDataModelToWidget('treeView', model)
        self.treeView.setUpdatesEnabled(True)
        self._active_model['treeView'].layoutChanged.emit()

    def _invokeMessageBoxAbout(self):
        QMessageBox.about(self, 'About', '')

    def _invokeMessageBoxLicense(self):
        QMessageBox.about(self, 'License', app_prefetch_license)

    def _invokeMessageBoxAboutQt(self):
        QMessageBox.aboutQt(self)

    def _invokeMessageBoxAtRoot(self):
        file_path, _ = self._wrapperFileDialog(
            "",
            "All Files (*);;DICOM Files (*.dcm)" 
            )()
        if file_path:
            self._handleAtFileOpen(file_path)

    def _invokeFileDialogAtTest(self):
        file_path, _ = self._wrapperFileDialog(
            test_preset_data_path,
            "All Files (*);;DICOM Files (*.dcm)" 
            )()
        if file_path:
            self._handleAtFileOpen(file_path)