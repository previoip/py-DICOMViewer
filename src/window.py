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
    QLabel,
    QPushButton,
    QCheckBox,
)

from PyQt5.QtCore import (
    Qt,
    QSize,
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

# from src.dicom_image_filter import (
#     DicomImageFilterContainer,
# )

from src.widget_matplotlib import (
    WidgetMplToolbar,
    WidgetMplCanvas
)

from src.widget_filter import QTreeItemWidgetFilter, _filters

import os
from pathlib import Path



class App_QMainWindow(QMainWindow):

    resize_signal = pyqtSignal()
    render_signal = pyqtSignal()

    def __init__(self, design_file='./mainwindow.ui'):

        # mental note
        # root attribute tree derived from mainwindow.ui
        # and is accessible from parent (MainWindow)
        # attributes:
        #
        # MainWindow (QMainWindow)
        # ├── centralwidget (QWidget)
        # │   ├── buttonFilterClear (QPushButton)
        # │   ├── buttonFilterDialog (QPushButton)
        # │   ├── frameMplRenderWidgetContainer (QFrame)
        # │   ├── frameToolbarWidgetContainer (QFrame)
        # │   ├── tableViewWDicomProperty (QTableWidget)
        # │   ├── treeViewWImageFilter (QToolBox)
        # │   └── treeViewVDicomRecords (QTreeView)
        # └── menubar (QMenuBar)
        #     ├── menuFile (QMenu)
        #     │   ├── actionFileDialogTest (QAction)
        #     │   ├── actionFileDialog (QAction)
        #     │   └── actionExit (QAction)
        #     └── menuAbout (QMenu)
        #         ├── actionModalAbout (QAction)
        #         ├── actionModalLicense (QAction)
        #         └── actionModalAboutQt (QAction)
        
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
        self._initTreeViewVDicomRecordsWidget()
        self._initTableViewWDicomProperty()
        self._initFrameMplRenderWidgetContainer()
        self._initTreeViewWImageFilter()

    def _initMenuBars(self):
        self.actionExit.triggered.connect(self._wrapperAtExit())
        self.actionModalAbout.triggered.connect(self._invokeMessageBoxAbout)
        self.actionModalLicense.triggered.connect(self._invokeMessageBoxLicense)
        self.actionModalAboutQt.triggered.connect(self._invokeMessageBoxAboutQt)
        self.actionFileDialog.triggered.connect(self._invokeMessageBoxAtRoot)
        self.actionFileDialogTest.triggered.connect(self._invokeFileDialogAtTest)

    def _initTreeViewVDicomRecordsWidget(self):
        self.treeViewVDicomRecords.selectionChanged = \
            lambda curr, prev: self._handleOnItemSelect(curr.indexes(), prev.indexes())

    def _initTableViewWDicomProperty(self):
        header = self.tableViewWDicomProperty.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def _initFrameMplRenderWidgetContainer(self):
        self.mplCanvas = WidgetMplCanvas(self.frameMplRenderWidgetContainer)
        self.mplToolbar = WidgetMplToolbar(self.mplCanvas, self.frameToolbarWidgetContainer)
        self.resize_signal.connect(self._invokeOnResizeEvent)
        self.render_signal.connect(self.invokeImageUpdate)
        self.mplToolbar.setOrientation(Qt.Vertical)

    def _initTreeViewWImageFilter(self):
        self.treeViewWImageFilter.resizeColumnToContents(0)
        self.treeViewWImageFilter.resizeColumnToContents(1)
        self._invokeNewFilter(0)
        self._invokeNewFilter(1)
        self._invokeNewFilter(2)

    # handlers

    def _invokeNewFilter(self, filter_enum=0):
        root = self.treeViewWImageFilter.invisibleRootItem()

        child = QTreeWidgetItem(root)
        child_filter = QTreeWidgetItem(child)
        widget = QTreeItemWidgetFilter(child_filter, filter_enum=filter_enum)
        destructorButton = QPushButton()
        destructorButton.setMaximumSize(QSize(16, 16))
        enableCheckBox = QCheckBox('')
        enableCheckBox.setChecked(True)
        enableCheckBox.stateChanged.connect(
            lambda x: widget.setEnabled(enableCheckBox.isChecked())
        )

        destructorButton.clicked.connect(widget._delete)
        self.treeViewWImageFilter.setItemWidget(child, 0, enableCheckBox)
        self.treeViewWImageFilter.setItemWidget(child, 1, destructorButton)
        self.treeViewWImageFilter.setItemWidget(child_filter, 0, widget)
        widget.filter_signal.connect(self.render_signal.emit)


        child.setText(2, widget.filter.displayName())

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
        table_widget = self.tableViewWDicomProperty
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

        canvas_widget.dispatchSetArr(ds_img)
        self.render_signal.emit()

    def invokeImageUpdate(self):
        ds =  self.mplCanvas.getDsWr()
        arr = ds.pixel_array.copy()


        for i in self.treeViewWImageFilter.selectedItems():
            print(i)
        print()
        for f in _filters:
            if f.isInplaceOp():
                f.dispatch(ds, arr)
            else:
                arr = f.dispatch(ds, arr)
        self.mplCanvas.setArr(arr)
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
        self.treeViewVDicomRecords.setUpdatesEnabled(False)

        model = self._active_model['treeViewVDicomRecords']
        root = model.getNode().getRootNode()
        self.setDataModelToWidget('treeViewVDicomRecords', None)

        self._active_path = file_path
        parseDicomFromPath(file_path, root)

        self.setDataModelToWidget('treeViewVDicomRecords', model)
        self.treeViewVDicomRecords.setUpdatesEnabled(True)
        self._active_model['treeViewVDicomRecords'].layoutChanged.emit()

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