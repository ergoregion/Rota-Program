__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal
from commands_role_compatibility import CommandChangeCompatibilityRole


class RoleCompatibilitiesSettingModel(QtCore.QAbstractTableModel):
    """
    used to manipulate the relative compatibilities between roles
    """

    commandIssued = pyqtSignal(QtGui.QUndoCommand)

    def __init__(self, all_roles_model):
        QtCore.QAbstractTableModel.__init__(self)
        self._allRolesModel = all_roles_model
        all_roles_model.rolelist.roleAdded.connect(self.roles_changed)
        all_roles_model.rolelist.roleRemoved.connect(self.roles_changed)
        all_roles_model.rolelist.rolesChanged.connect(self.roles_changed)
        for r in all_roles_model.rolelist.roles:
            r.compatibilitiesChanged.connect(self.role_changed)

    @QtCore.pyqtSlot()
    def roles_changed(self):
        self.reset()
        for r in self._allRolesModel.rolelist.roles:
            r.compatibilitiesChanged.connect(self.role_changed)

    @QtCore.pyqtSlot()
    def role_changed(self):
        self.reset()

    def columnCount(self, index):
        return len(self._allRolesModel.rolelist.roles)

    def rowCount(self, index):
        return len(self._allRolesModel.rolelist.roles)

    def flags(self, index):
        return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if not (role == QtCore.Qt.CheckStateRole):
            return None
        role1 = self._allRolesModel.rolelist.roles[index.row()]
        role2 = self._allRolesModel.rolelist.roles[index.column()]
        return role1.compatible_with(role2)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if not (role == QtCore.Qt.DisplayRole):
            return None
        return self._allRolesModel.rolelist.roles[section].description

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return False
        if not (role == QtCore.Qt.CheckStateRole):
            return False
        role1 = self._allRolesModel.rolelist.roles[index.row()]
        role2 = self._allRolesModel.rolelist.roles[index.column()]
        compatible = role1.compatible_with(role2)
        command = CommandChangeCompatibilityRole(role1, role2, not compatible)
        self.commandIssued.emit(command)
        return True
