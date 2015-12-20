__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui


class MasterUndoModel(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.undoStack = QtGui.QUndoStack(self)

    def add_command_contributer(self, other_model):
        other_model.commandIssued.connect(self.add_command_to_stack)
        other_model.criticalCommandIssued.connect(self.clear_stack)

    def remove_command_contributer(self, other_model):
        other_model.commandIssued.disconnect(self.add_command_to_stack)
        other_model.criticalCommandIssued.disconnect(self.clear_stack)

    @QtCore.pyqtSlot()
    def undo(self):
        self.undoStack.undo()

    @QtCore.pyqtSlot()
    def redo(self):
        self.undoStack.redo()

    @QtCore.pyqtSlot(QtGui.QUndoCommand)
    def add_command_to_stack(self, command):
        self.undoStack.push(command)

    @QtCore.pyqtSlot()
    def clear_stack(self):
        self.undoStack.clear()