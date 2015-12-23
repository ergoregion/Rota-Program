__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from commands_population import CommandAddPerson


class PopulationModel(QtCore.QAbstractListModel):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.population = parent.people
        for p in self.population:
            p.nameChanged.connect(self.person_name_changed)

    def rowCount(self, parent):
        return len(self.population)

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != QtCore.Qt.DisplayRole:
            return None
        person = self.population[index.row()]
        return QtCore.QVariant(person.name)

    def object(self, index):
        return self.population[index.row()]

    def criticalDelete(self):
        return True

    def insertRow(self, row, parent=QtCore.QModelIndex()):
        command = CommandAddPerson(self, row, parent)
        self.commandIssued.emit(command)

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row)
        removed_person = self.population.pop(row)
        removed_person.nameChanged.disconnect(self.person_name_changed)
        self.endRemoveRows()
        self.criticalCommandIssued.emit()

    @QtCore.pyqtSlot(QtCore.QObject)
    def person_name_changed(self, person):
        i = self.population.index(person)
        index = self.index(i)
        self.dataChanged.emit(index, index)