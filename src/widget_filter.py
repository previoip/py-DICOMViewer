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
        self.parent=parent
        uic.loadUi(design_file, self)
        self.setAutoFillBackground(True)
        if isinstance(self.parent, QTreeWidgetItem):
            flags = self.parent.flags()
            flags &= Qt.ItemIsSelectable
            flags &= Qt.ItemIsUserCheckable
            flags &= Qt.ItemIsEditable
            flags &= Qt.ItemIsDragEnabled 
            flags &= Qt.ItemIsDropEnabled 

            self.parent.setFlags(flags)
