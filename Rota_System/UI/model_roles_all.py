__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal

class AllRolesModel(QtCore.QAbstractListModel):
    '''
    used to manipulate The Complete global list of roles
    '''

    aboutToAddRole = pyqtSignal()
    addRole = pyqtSignal()
    aboutToRemoveRole = pyqtSignal(str)
    removeRole = pyqtSignal(str)

    commandIssued = pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = pyqtSignal()


    def __init__(self,allRolelist):
        super(QtCore.QAbstractListModel, self).__init__()
        self.rolelist = allRolelist
        allRolelist.rolesChanged.connect(self.reset)

    def columnCount(self, index):
        return 1

    def rowCount(self, index):
        return len(self.rolelist.roles)

    def headerData(self,section, orientation, role):
        return None

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if role != QtCore.Qt.DisplayRole:
            return None

        if index.column() == 0 :
            return self.rolelist.roles[index.row()].description
        else :
            return QtCore.QVariant()

    def criticalDelete(self):
        return True

    def insertRow(self, row,   parent =QtCore.QModelIndex()):
        command = CommandAddRole(self, row,parent)
        self.commandIssued.emit(command)

    def object(self, index):
        return self.rolelist.roles[index.row()]

    def removeRow(self, row,   parent =QtCore.QModelIndex()):
        role = self.rolelist.roles[row]
        self.aboutToRemoveRole.emit(role.code)
        self.beginRemoveRows(parent, row, row)
        self.rolelist.removeRole(role)
        self.endRemoveRows()
        self.removeRole.emit(role.code)
        self.criticalCommandIssued.emit()