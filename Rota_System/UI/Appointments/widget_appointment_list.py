__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from Rota_System.Roles import GlobalRoleList
from model_appointment_list import AppointmentsTableModel
from Rota_System.UI.widget_addDel_table import AddDelTableWidget


def description(role):
    return role.description


class AppointmentsListWidget(QtGui.QWidget):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QGridLayout(self)

        self.rolesComboBox = QtGui.QComboBox(self)
        self.rolesComboBox.activated.connect(self.roleSelected)
        self.layout.addWidget(self.rolesComboBox, 0, 0, 1, 1)

        self.tableWidget = AddDelTableWidget(self)
        self.layout.addWidget(self.tableWidget, 1, 0, 1, 2)

        self.reset()
        GlobalRoleList.rolesChanged.connect(self.reset)
        self.setModel(AppointmentsTableModel(self))

    @QtCore.pyqtSlot(int)
    def roleSelected(self, i):
        role = GlobalRoleList.roles[i]
        self.tableWidget.getModel().roleSelected(role)

    @QtCore.pyqtSlot(int)
    def reset(self):
        self.rolesComboBox.clear()
        self.rolesComboBox.insertItems(0, map(description, GlobalRoleList.roles))

    def setModel(self, model):
        self.tableWidget.setModel(model)
        model.commandIssued.connect(self.emitCommand)
        model.criticalCommandIssued.connect(self.emitCriticalCommand)

    def setEvent(self, newEvent):
        self.tableWidget.getModel().setEvent(newEvent)

    @QtCore.pyqtSlot(QtGui.QUndoCommand)
    def emitCommand(self, command):
        self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def emitCriticalCommand(self):
        self.criticalCommandIssued.emit()


import sys
from Rota_System.Roles import Role
from Rota_System import Events
from Rota_System.UI.model_undo import MasterUndoModel


def main():
    GlobalRoleList.add_role(Role('Baker', 'B', 2))
    GlobalRoleList.add_role(Role('Steward', 'S', 9))
    GlobalRoleList.add_role(Role('Fisherman', 'F', 7))

    m = MasterUndoModel()

    app = QtGui.QApplication(sys.argv)
    w = AppointmentsListWidget(None)
    am = AppointmentsTableModel(w)

    e = Events.Event(None)
    am.setEvent(e)
    w.setModel(am)
    m.add_command_contributer(w)
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()