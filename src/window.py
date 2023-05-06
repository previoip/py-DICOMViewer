from PyQt5 import (
    QtWidgets,
    uic
)

from PyQt5.QtWidgets import (
    qApp,
    QWidget,
    QMainWindow,
    QTableView,
    QHeaderView,
    QMessageBox,
    QFileDialog,
    QTableWidgetItem,
    QTreeWidgetItem,
    QLabel
)

from PyQt5.QtCore import (
    Qt,
    pyqtSignal,
)

import numpy as np
import matplotlib.pyplot as plt

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

from src.dicom_image_filter import (
    DicomImageFilterContainer,
    DicomImageFilterFlags
)

from src.widget_matplotlib import (
    WidgetMplToolbar,
    WidgetMplCanvas
)

from src.widget_filter import QTreeItemWidgetFilter

import os
from pathlib import Path



class App_QMainWindow(QMainWindow):

    resize_signal = pyqtSignal()
    render_signal = pyqtSignal()

    def __init__(self, design_file='./mainwindow.ui'):

        # mental note
        # root attribute tree derived from mainwindow.ui:
        #
        # MainWindow  (QMainWindow)
        # ├── centralwidget (QWidget)
        # │   ├── mplFrame (QFrame)
        # │   ├── tableDicomProps (QTableWidget)
        # │   ├── DicomImageFilterTree (QToolBox)
        # │   ├── toolbarFrameMplCanvas (QFrame)
        # │   └── treeViewDicomRecords (QTreeView)
        # └── menubar (QMenuBar)
        #     ├── menuFile (QMenu)
        #     │   ├── actionOpen_Test (QAction)
        #     │   ├── actionOpen (QAction)
        #     │   └── actionExit (QAction)
        #     └── menuAbout (QMenu)
        #         ├── actionAbout (QAction)
        #         ├── actionLicense (QAction)
        #         └── actionAbout_Qt (QAction)
        
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
        self._initTreeViewDicomRecordsWidget()
        self._initTableDicomProps()
        self._initMplCanvas()
        self._initFilterDicomImageFilterTree()

    def _initMenuBars(self):
        self.actionExit.triggered.connect(self._wrapperAtExit())
        self.actionAbout.triggered.connect(self._invokeMessageBoxAbout)
        self.actionLicense.triggered.connect(self._invokeMessageBoxLicense)
        self.actionAbout_Qt.triggered.connect(self._invokeMessageBoxAboutQt)
        self.actionOpen.triggered.connect(self._invokeMessageBoxAtRoot)
        self.actionOpen_Test.triggered.connect(self._invokeFileDialogAtTest)

    def _initTreeViewDicomRecordsWidget(self):
        # self.treeViewDicomRecords.activated.connect(self._handleOnItemSelect)
        self.treeViewDicomRecords.selectionChanged = \
            lambda curr, prev: self._handleOnItemSelect(curr.indexes(), prev.indexes())

    def _initTableDicomProps(self):
        header = self.tableDicomProps.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def _initMplCanvas(self):
        self.mplCanvas = WidgetMplCanvas(self.mplFrame)
        self.mplToolbar = WidgetMplToolbar(self.mplCanvas, self.toolbarFrameMplCanvas)
        self.resize_signal.connect(self._invokeOnResizeEvent)
        self.render_signal.connect(self.invokeImageUpdate)
        self.mplToolbar.setOrientation(Qt.Vertical)

    def _initFilterDicomImageFilterTree(self):
        for i in range(3):
            child = QTreeWidgetItem(self.DicomImageFilterTree)
            child.setText(0, f'imagefilter {i}')
            child.setText(1, f'None')
            child_filter = QTreeWidgetItem(child)
            widget = QTreeItemWidgetFilter(child_filter)
            self.DicomImageFilterTree.setItemWidget(child_filter, 0, widget)

    # handlers

    def _invokeOnResizeEvent(self):
        self.mplCanvas.resizeFitToParentWidget()

    def _handleOnItemSelect(self, current_indexes, previous_indexes):
        for curr in current_indexes:
            curr.internalPointer().active = True
            self._handleLoadDicomData(curr)
            self._handleLoadDsToTable(curr)
        
        for prev in previous_indexes:
            prev.internalPointer().active = False

    def _handleLoadDsToTable(self, index):
        table_widget = self.tableDicomProps
        dicom_node = index.internalPointer()

        row = table_widget.rowCount()
        for i in range(row):
            table_widget.removeRow(i)

        ds = dicom_node.getObj()
        els = [i for i in ds]
        table_widget.setRowCount(len(els))

        for r, el in enumerate(els):
            table_widget.setItem(r, 0, QTableWidgetItem(el.name))
            table_widget.setItem(r, 1, QTableWidgetItem(el.repval))

    def _handleLoadDicomData(self, index):
        canvas_widget = self.mplCanvas

        dicom_node = index.internalPointer()

        if not dicom_node.isObjAccessible():
            return

        root_dicom_node = dicom_node.getRootNode().getChild(0)
        root_dicom_path = Path(root_dicom_node.getObj().filename)
        ds = dicom_node.getObj()
        
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
        filter_container = DicomImageFilterContainer(ds_img)
        canvas_widget.dispatchSetArr(filter_container)
        self.render_signal.emit()

    def invokeImageUpdate(self):
        self.mplCanvas.updateImage()

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
        self.treeViewDicomRecords.setUpdatesEnabled(False)

        model = self._active_model['treeViewDicomRecords']
        root = model.getNode().getRootNode()
        self.setDataModelToWidget('treeViewDicomRecords', None)

        self._active_path = file_path
        parseDicomFromPath(file_path, root)

        self.setDataModelToWidget('treeViewDicomRecords', model)
        self.treeViewDicomRecords.setUpdatesEnabled(True)
        self._active_model['treeViewDicomRecords'].layoutChanged.emit()

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