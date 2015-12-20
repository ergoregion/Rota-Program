__author__ = 'Neil Butcher'

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal

from model_roles_all import AllRolesModel
from Rota_System.UI.Roles.commands_roles_sublist import CommandExcludeRole, CommandIncludeRole


class SelectionOfRolesModel(AllRolesModel):
    """
    used to manipulate a selection of the roles
    """

    commandIssued = pyqtSignal(QtGui.QUndoCommand)

    def __init__(self, all_roles_list, rolelist):
        AllRolesModel.__init__(all_roles_list)
        self.roleListSelection = rolelist
        rolelist.rolesChanged.connect(self.roles_changed)

    @QtCore.pyqtSlot()
    def roles_changed(self):
        self.reset()

    def flags(self, index):
        return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if not ((role == QtCore.Qt.DisplayRole) | (role == QtCore.Qt.CheckStateRole)):
            return None

        if index.column() == 0:
            if role == QtCore.Qt.DisplayRole:
                return self.rolelist.roles[index.row()].description
            if role == QtCore.Qt.CheckStateRole:
                return self.roleListSelection.includes(self.rolelist.roles[index.row()])
            else:
                return QtCore.QVariant()
        else:
            return QtCore.QVariant()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return False
        if not (role == QtCore.Qt.CheckStateRole):
            return False
        if index.column() == 0:
            if not self.data(index, role):
                command = CommandIncludeRole(self.roleListSelection, self.rolelist.roles[index.row()])
                self.commandIssued.emit(command)
            else:
                command = CommandExcludeRole(self.roleListSelection, self.rolelist.roles[index.row()])
                self.commandIssued.emit(command)
        else:
            return False
        return True