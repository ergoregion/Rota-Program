__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from command_duration import CommandChangeDuration
from command_durations import CommandAddDuration, CommandRemoveDuration
from Rota_System.Duration import Duration


class DurationsModel(QtCore.QAbstractListModel):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(QtCore.QAbstractListModel, self).__init__(parent)
        self.institution = parent

        for p in self.durations:
            p.nameChanged.connect(self._durationNameChanged)

    @property
    def durations(self):
        return self.institution.durations

    def rowCount(self, parent):
        return len(self.durations)

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != QtCore.Qt.DisplayRole:
            return None
        durat = self.durations[index.row()]
        return QtCore.QVariant(durat.name)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return None

        durat = self.durations[index.row()]

        if index.column() == 0 and role == QtCore.Qt.EditRole:
            command = CommandChangeDuration(durat, 'name', str(value))
            self.commandIssued.emit(command)
            return True
        else:
            return None

    @property
    def objects(self):
        return self.durations

    def criticalDelete(self):
        return False

    def newDuration(self):
        duration = Duration(self.institution)
        return duration

    def insertRow(self, row, parent=QtCore.QModelIndex()):
        command = CommandAddDuration(self, row, parent)
        self.commandIssued.emit(command)

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        command = CommandRemoveDuration(self, row, parent)
        self.commandIssued.emit(command)

    @QtCore.pyqtSlot(QtCore.QObject)
    def _durationNameChanged(self, durat):
        i = self.durations.index(durat)
        index = self.index(i)
        self.dataChanged.emit(index, index)
