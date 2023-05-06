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


class QTreeItemWidgetFilter(QWidget):
    def __init__(self, parent=None, design_file='src/ui/filter.ui'):
        super().__init__()
        if not isinstance(parent, QTreeWidgetItem):
            raise ValueError('parent is not QTreeWidgetItem')
        self._parent=parent
        uic.loadUi(design_file, self)
        self.setAutoFillBackground(True)
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