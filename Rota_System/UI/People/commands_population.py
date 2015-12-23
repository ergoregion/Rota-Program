__author__ = 'Neil Butcher'

from PyQt4 import QtGui
from Rota_System.Worker import Worker


class CommandAddPerson(QtGui.QUndoCommand):
    def __init__(self, model, row, parent):
        super(CommandAddPerson, self).__init__('Added a new person')
        self.model = model
        self.row = row
        self.parent = parent
        self.person = Worker()

    def redo(self):
        self.model.beginInsertRows(self.parent, self.row, self.row)
        self.model.population.insert(self.row, self.person)
        self.person.nameChanged.connect(self.model.person_name_changed)
        self.model.endInsertRows()

    def undo(self):
        self.model.beginRemoveRows(self.parent, self.row, self.row)
        self.model.population.pop(self.row)
        self.person.nameChanged.disconnect(self.model.person_name_changed)
        self.model.endRemoveRows()