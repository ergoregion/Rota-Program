__author__ = 'Neil Butcher'

import sys
from PyQt4 import QtGui, QtCore, uic
from model_roles_all import AllRolesModel
from model_role_compatibility import RoleCompatibilitiesSettingModel
from Rota_System.Roles import GlobalRoleList


class GlobalRolesWidget(QtGui.QWidget):

    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi('widget_roles_all.ui', self)
        self.listWidget.objectSelected.connect(self.singleRoleWidget.role)
        self.singleRoleWidget.commandIssued.connect(self.emitCommand)
        self.setupModels()

    def setupModels(self):
        model = AllRolesModel(GlobalRoleList)
        self.listWidget.setModel(model)
        model.commandIssued.connect(self.emitCommand)
        model.criticalCommandIssued.connect(self.emitCriticalCommand)
        compatibilitiesModel = RoleCompatibilitiesSettingModel(model)
        self.tableView.setModel(compatibilitiesModel)
        compatibilitiesModel.commandIssued.connect(self.emitCommand)

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

    app = QtGui.QApplication(sys.argv)
    w = GlobalRolesWidget(None)
    w.setWindowTitle('roles')
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
