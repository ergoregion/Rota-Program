__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from model_undo import MasterUndoModel


class UndoBarWidget(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

        self.model = MasterUndoModel(parent)
        self.layout = QtGui.QHBoxLayout(self)

        self.undoPushButton = QtGui.QPushButton('Undo', self)
        self.undoPushButton.clicked.connect(self.undo)
        self.layout.addWidget(self.undoPushButton)
        self.model.undoStack.canUndoChanged.connect(self.updateUndoButton)

        self.redoPushButton = QtGui.QPushButton('Redo', self)

        self.redoPushButton.clicked.connect(self.redo)
        self.layout.addWidget(self.redoPushButton)
        self.model.undoStack.canRedoChanged.connect(self.updateRedoButton)

    @QtCore.pyqtSlot()
    def undo(self):
        self.model.undo()
        return True

    @QtCore.pyqtSlot()
    def redo(self):
        self.model.redo()
        return True

    @QtCore.pyqtSlot(bool)
    def updateRedoButton(self, boolean):
        self.redoPushButton.setEnabled(boolean)
        return True

    @QtCore.pyqtSlot(bool)
    def updateUndoButton(self, boolean):
        self.undoPushButton.setEnabled(boolean)
        return True
