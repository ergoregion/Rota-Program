__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from Rota_System.StandardTimes import StandardEventTimes
from commands_times import CommandAddStandardTime, CommandChangeStandardTime, CommandRemoveStandardTime
from datetime import time


class StandardEventTimesModel(QtCore.QAbstractTableModel):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(StandardEventTimesModel, self).__init__(parent)

    def rowCount(self, index):
        return len(StandardEventTimes)

    def columnCount(self, index):
        return 2

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        item = StandardEventTimes[index.row()]

        if role != QtCore.Qt.DisplayRole:
            return None

        if index.column() == 0:
            return QtCore.QVariant(str(item[0]))
        elif index.column() == 1:
            return QtCore.QVariant(item[1].strftime("%H:%M"))
        else:
            return QtCore.QVariant()

    def object(self, index):
        return None

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def criticalDelete(self):
        return False

    def headerData(self, section, orientation, role):
        return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return None
        if role != QtCore.Qt.EditRole:
            return None

        if index.column() == 0:
            string_value = str(value.toString())
            if string_value == '' or string_value == StandardEventTimes[index.row()][0]:
                return True
            item = string_value, StandardEventTimes[index.row()][1]
            command = CommandChangeStandardTime(self, index.row(), item)
            self.commandIssued.emit(command)
            return True

        if index.column() == 1:
            if value == StandardEventTimes[index.row()][1]:
                return True
            item = StandardEventTimes[index.row()][0], value
            command = CommandChangeStandardTime(self, index.row(), item)
            self.commandIssued.emit(command)
            return True
        else:
            return None

    def insertRow(self, row, parent=QtCore.QModelIndex()):
        command = CommandAddStandardTime(self, row, ('new time', time(00, 00, 00)))
        self.commandIssued.emit(command)

    def objects(self):
        return StandardEventTimes

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        command = CommandRemoveStandardTime(self, row, self.objects()[row])
        self.commandIssued.emit(command)