__author__ = 'Neil Butcher'

from PyQt4 import QtGui

class CommandAddDuration(QtGui.QUndoCommand):
    def __init__(self, model, row, parent):
        super(CommandAddDuration, self).__init__('Added a new duration')
        self.model = model
        self.row = row
        self.parent = parent
        self.duration = model.newDuration()

    def redo(self):
        self.model.beginInsertRows(self.parent, self.row, self.row)
        self.model.durations.insert(self.row, self.duration)
        self.duration.nameChanged.connect(self.model._durationNameChanged)
        self.model.endInsertRows()

    def undo(self):
        self.model.beginRemoveRows(self.parent, self.row, self.row)
        self.model.durations.pop(self.row)
        self.duration.nameChanged.disconnect(self.model._durationNameChanged)
        self.model.endRemoveRows()

class CommandRemoveDuration(QtGui.QUndoCommand):
    def __init__(self, model, row, parent):
        super(CommandRemoveDuration, self).__init__('Removed a duration')
        self.model = model
        self.row = row
        self.parent = parent
        self.duration = model.durations[row]

    def undo(self):
        self.model.beginInsertRows(self.parent, self.row, self.row)
        self.model.durations.insert(self.row, self.duration)
        self.duration.nameChanged.connect(self.model._durationNameChanged)
        self.model.endInsertRows()

    def redo(self):
        self.model.beginRemoveRows(self.parent, self.row, self.row)
        self.model.durations.pop(self.row)
        self.duration.nameChanged.disconnect(self.model._durationNameChanged)
        self.model.endRemoveRows()