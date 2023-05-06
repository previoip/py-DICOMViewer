from PyQt5 import (
    QtWidgets,
    uic
)
from PyQt5.QtWidgets import (
    QWidget,
    QTreeWidgetItem,
    QLabel,
)
from PyQt5.QtCore import (
    Qt
)

from src.dicom_image_filter import (
    dicom_image_filters,
    newFilter
)

class QTreeItemWidgetFilter(QWidget):
    def __init__(self, parent, design_file='src/ui/filter.ui', filter_enum=0):
        if not isinstance(parent, QTreeWidgetItem):
            raise ValueError('parent is not QTreeWidgetItem')

        super().__init__()
        uic.loadUi(design_file, self)
        self.setAutoFillBackground(True)
        self._parent = parent
        self.filter = newFilter(filter_enum)
        flags = self._parent.flags()
        flags &= not Qt.ItemIsSelectable
        flags &= not Qt.ItemIsUserCheckable
        flags &= not Qt.ItemIsEditable
        flags &= not Qt.ItemIsDragEnabled 
        flags &= not Qt.ItemIsDropEnabled 
        self._parent.setFlags(flags)

        self.buttonDelete.clicked.connect(self._delete)

    def _delete(self):
        widget_parent = self._parent.treeWidget()
        root = widget_parent.invisibleRootItem()
        widget_parent.removeItemWidget(self._parent, 0)
        root.removeChild(self._parent.parent())