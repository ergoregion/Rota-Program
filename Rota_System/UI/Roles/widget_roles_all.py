__author__ = 'Neil Butcher'

import sys

from PyQt4 import QtGui, QtCore

from Rota_System.UI.Roles.model_roles_all import AllRolesModel
from model_role_compatibility import RoleCompatibilitiesSettingModel
from Rota_System.Roles import GlobalRoleList, Role
from Rota_System.UI.widget_addDel_list import AddDelListWidget
from Rota_System.UI.model_undo import MasterUndoModel
from widget_role import SingleRoleWidget


class GlobalRolesWidget(QtGui.QWidget):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.layout = QtGui.QGridLayout(self)
        self.listWidget = AddDelListWidget(self)
        self.layout.addWidget(self.listWidget, 0, 0, 2, 2)
        self.singleRoleWidget = SingleRoleWidget(self)
        self.layout.addWidget(self.singleRoleWidget, 0, 2, 1, 1)
        self.tableView = QtGui.QTableView(self)
        self.layout.addWidget(self.tableView, 1, 2, 1, 1)

        self.listWidget.objectSelected.connect(self.singleRoleWidget.role)
        self.singleRoleWidget.commandIssued.connect(self.emitCommand)
        self.setup_models()

    def setup_models(self):
        model = AllRolesModel(GlobalRoleList)
        self.listWidget.setModel(model)
        model.commandIssued.connect(self.emitCommand)
        model.criticalCommandIssued.connect(self.emitCriticalCommand)
        compatibilities_model = RoleCompatibilitiesSettingModel(model)
        self.tableView.setModel(compatibilities_model)
        compatibilities_model.commandIssued.connect(self.emitCommand)

    @QtCore.pyqtSlot(QtGui.QUndoCommand)
    def emitCommand(self, command):
        self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def emitCriticalCommand(self):
        self.criticalCommandIssued.emit()

    def institution(self, i):
        self.listWidget.update()
        self.tableView.update()


def main():
    GlobalRoleList.add_role(Role('Baker', 'B', 2))
    GlobalRoleList.add_role(Role('Steward', 'S', 9))
    GlobalRoleList.add_role(Role('Fisherman', 'F', 7))

    m = MasterUndoModel()

    app = QtGui.QApplication(sys.argv)
    w = GlobalRolesWidget(None)
    m.add_command_contributer(w)
    w.setWindowTitle('roles')
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
