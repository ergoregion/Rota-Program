__author__ = 'Neil Butcher'

from PyQt4 import QtGui, QtCore
from Rota_System.StandardTimes import StandardEventTimes


class CommandAddStandardTime(QtGui.QUndoCommand):
    def __init__(self, model, row, item):
        QtGui.QUndoCommand.__init__(self, 'Added a new time with a name')
        self.model = model
        self.row = row
        self.item = item

    def redo(self):
        self.model.beginInsertRows(QtCore.QModelIndex(), self.row, self.row)
        StandardEventTimes.append(self.item)
        self.model.endInsertRows()

    def undo(self):
        self.model.beginRemoveRows(QtCore.QModelIndex(), self.row, self.row)
        StandardEventTimes.remove(self.item)
        self.model.endRemoveRows()


class CommandRemoveStandardTime(QtGui.QUndoCommand):
    def __init__(self, model, row, item):
        QtGui.QUndoCommand.__init__(self, 'Removed a named time')
        self.model = model
        self.row = row
        self.item = item

    def redo(self):
        self.model.beginRemoveRows(QtCore.QModelIndex(), self.row, self.row)
        StandardEventTimes.remove(self.item)
        self.model.endRemoveRows()

    def undo(self):
        self.model.beginInsertRows(QtCore.QModelIndex(), self.row, self.row)
        StandardEventTimes.append(self.item)
        self.model.endInsertRows()


class CommandChangeStandardTime(QtGui.QUndoCommand):
    def __init__(self, model, row, item):
        QtGui.QUndoCommand.__init__(self, 'Altered a named time')
        self.model = model
        self.row = row
        self.item = item
        self.previousItem = StandardEventTimes[row]

    def redo(self):
        StandardEventTimes[self.row] = self.item
        self.model.dataChanged.emit(self.model.index(self.row, 0), self.model.index(self.row, 1))

    def undo(self):
        StandardEventTimes[self.row] = self.previousItem
        self.model.dataChanged.emit(self.model.index(self.row, 0), self.model.index(self.row, 1))