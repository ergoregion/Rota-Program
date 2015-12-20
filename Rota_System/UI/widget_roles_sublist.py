__author__ = 'Neil Butcher'

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal
from Rota_System.Roles import Role, GlobalRoleList
from model_roles_sublist import SelectionOfRolesModel

class RoleListWidget(QtGui.QWidget):

    roleSelected = pyqtSignal(Role)

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QHBoxLayout(self)
        self.roles = QtGui.QListBox(self)
        self.layout.addWidget(self.roles)
        self.roles.clicked.connect(self.role_clicked)

    def roleList(self,role_list):
        model = SelectionOfRolesModel(GlobalRoleList,role_list)
        self.setModel(model)
        return model

    def setModel(self,model):
        self.model = model
        self.roles.setModel(model)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def role_clicked(self,index):
        r= self.model.rolelist.roles[index.row()]
        self.roleSelected.emit(r)