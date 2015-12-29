__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui


class AddDelTableWidget(QtGui.QWidget):
    objectSelected = QtCore.pyqtSignal(QtCore.QObject)

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QGridLayout(self)
        self.tableView = QtGui.QTableView(self)
        self.tableView.clicked.connect(self.cellSelected)
        self.layout.addWidget(self.tableView, 0, 0, 1, 2)
        self.add_button = QtGui.QPushButton('Add', self)
        self.add_button.clicked.connect(self.addButtonPressed)
        self.layout.addWidget(self.add_button, 1, 0, 1, 1)
        self.del_button = QtGui.QPushButton('Delete', self)
        self.del_button.clicked.connect(self.delButtonPressed)
        self.layout.addWidget(self.del_button, 1, 1, 1, 1)
        self._model = None

    def setModel(self, model):
        self._model = model
        self.tableView.setModel(model)

    def getModel(self):
        return self._model

    @QtCore.pyqtSlot()
    def addButtonPressed(self):
        self._model.insertRow(self._model.rowCount(None))
        index = self._model.index((self._model.rowCount(None) - 1), 0)
        self.tableView.setCurrentIndex(index)

    @QtCore.pyqtSlot()
    def delButtonPressed(self):
        if self._model.criticalDelete():
            reply = QtGui.QMessageBox.question(self, 'This process is too profound to undo',
                                               "This will clear your undo stack, do you wish to proceeed?",
                                               QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return False
        self._model.removeRow(self.tableView.currentIndex().row())
        return True

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def cellSelected(self, index):
        self.objectSelected.emit(self._model.object(index))

    def setItemDelegateForRow(self, row, delegate):
        self.tableView.setItemDelegateForRow(row, delegate)

    def setItemDelegateForColumn(self, row, delegate):
        self.tableView.setItemDelegateForColumn(row, delegate)
