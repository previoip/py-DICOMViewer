from PyQt5 import (
    QtWidgets,
    uic
)
from PyQt5.QtWidgets import (
    QDialog,
    QTableWidgetItem,
    QDialogButtonBox,
)
from PyQt5.QtCore import (
    Qt,
    pyqtSignal
)

from src.dicom_image_filter import (
    dicom_image_filters,
)

class FilterEnumDialog(QDialog):
    def __init__(self, parent, design_file='src/ui/listdialog.ui'):
        super().__init__(parent=parent)
        uic.loadUi(design_file, self)
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem())
        self.tableWidget.horizontalHeaderItem(0).setText('Filter')
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem())
        self.tableWidget.horizontalHeaderItem(1).setText('Description')
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.__res = 0

        self.__button_ok = self.buttonBox.button(QDialogButtonBox.Ok)

        for n in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(n)
        self.tableWidget.setRowCount(len(dicom_image_filters))

        self.__items = []

        for n, fil in enumerate(dicom_image_filters):
            self.__items.append(QTableWidgetItem(fil._display_name))
            self.tableWidget.setItem(n, 0, self.__items[-1])
            self.__items.append(QTableWidgetItem(fil._display_desc))
            self.tableWidget.setItem(n, 1, self.__items[-1])

        self.tableWidget.itemClicked.connect(self._singleClicked)
        self.tableWidget.itemDoubleClicked.connect(self._doubleClicked)

    def resetStates(self):
        self.__button_ok.setEnabled(False)
        self.__res = 0
        for i in self.__items:
            i.setSelected(False)

    def _singleClicked(self, item):
        self.__res = item.row()
        self.__button_ok.setEnabled(item.isSelected())

    def _doubleClicked(self, item):
        self.__res = item.row()
        self.accept()
    
    def res(self):
        return self.__res