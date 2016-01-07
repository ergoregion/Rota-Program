__author__ = 'Neil Butcher'

from PyQt4 import QtGui, QtCore


def string(item): return str(item)


class AddDelComboWidget(QtGui.QWidget):
    objectSelected = QtCore.pyqtSignal(QtCore.QObject)

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QHBoxLayout(self)

        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.editTextChanged.connect(self.textChanged)
        self.comboBox.activated.connect(self.itemSelected)
        self.comboBox.currentIndexChanged.connect(self.itemSelected)
        self.layout.addWidget(self.comboBox)

        self.toolButton = QtGui.QPushButton('...', self)
        self.toolButton.setFixedWidth(40)
        self.toolButton.clicked.connect(self.editButtonPressed)
        self.layout.addWidget(self.toolButton)

        self.addButton = QtGui.QPushButton('+', self)
        self.addButton.setFixedWidth(40)
        self.addButton.clicked.connect(self.addButtonPressed)
        self.layout.addWidget(self.addButton)

        self.delButton = QtGui.QPushButton('-', self)
        self.delButton.setFixedWidth(40)
        self.delButton.clicked.connect(self.delButtonPressed)
        self.layout.addWidget(self.delButton)

        self._model = None

    def setModel(self, model):
        if self._model:
            self._model.rowsInserted.disconnect(self._resetList)
            self._model.rowsRemoved.disconnect(self._resetList)

        self._model = model
        self._model.rowsInserted.connect(self._resetList)
        self._model.rowsRemoved.connect(self._resetList)
        self._resetList()

    @QtCore.pyqtSlot()
    def _resetList(self):
        self.comboBox.clear()
        self.comboBox.addItems(map(string, self._model.objects))

    @QtCore.pyqtSlot()
    def addButtonPressed(self):
        self._model.insertRow(self._model.rowCount(None))
        self._resetList()
        return True

    @QtCore.pyqtSlot()
    def editButtonPressed(self):
        row = self.comboBox.currentIndex()
        index = self._model.createIndex(row, 0)
        currentText = string(self._model.objects[row])
        dlg = (QtGui.QInputDialog(self).getText(self, '', '', QtGui.QLineEdit.Normal, currentText))
        newString = str(dlg[0])
        if dlg[1] and not newString == currentText:
            self._model.setData(index, newString, QtCore.Qt.EditRole)
            self._resetList()

    @QtCore.pyqtSlot()
    def delButtonPressed(self):
        if self._model.criticalDelete():
            reply = QtGui.QMessageBox.question(self, 'This process is too profound to undo',
                                               "This will clear your undo stack, do you wish to proceeed?",
                                               QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No: return False
        self._model.removeRow(self.comboBox.currentIndex())
        self._resetList()
        return True

    @QtCore.pyqtSlot(int)
    def itemSelected(self, index):
        if len(self._model.objects) > 0:
            self.objectSelected.emit(self._model.objects[index])

    @QtCore.pyqtSlot(QtCore.QString)
    def textChanged(self, newString):
        row = self.comboBox.currentIndex()
        index = self._model.createIndex(row, 0)
        if not newString == string(self._model.objects[row]):
            self._model.setData(index, newString, QtCore.Qt.EditRole)
        self._resetList()
