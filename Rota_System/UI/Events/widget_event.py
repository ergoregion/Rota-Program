__author__ = 'Neil Butcher'

from PyQt4 import QtGui, QtCore
import widget_core
from Rota_System.UI.Appointments.widget_appointment_list import AppointmentsListWidget


class EventWidget(QtGui.QWidget):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QVBoxLayout(self)
        self.core_widget = widget_core.EventWidget(self)
        self.layout.addWidget(self.core_widget)
        self.core_widget.commandIssued.connect(self.emitCommand)
        self.core_widget.criticalCommandIssued.connect(self.emitCriticalCommand)

        self.appointment_widget = AppointmentsListWidget(self)
        self.layout.addWidget(self.appointment_widget)
        self.appointment_widget.commandIssued.connect(self.emitCommand)
        self.appointment_widget.criticalCommandIssued.connect(self.emitCriticalCommand)


    @QtCore.pyqtSlot(QtCore.QObject)
    def setEvent(self, item):
        self.core_widget.setEvent(item)
        self.appointment_widget.setEvent(item)

    @QtCore.pyqtSlot(QtGui.QUndoCommand)
    def emitCommand(self, command):
        self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def emitCriticalCommand(self):
        self.criticalCommandIssued.emit()



import sys
from Rota_System.Roles import Role, GlobalRoleList
from Rota_System import Events
from Rota_System.UI.model_undo import MasterUndoModel


def main():
    GlobalRoleList.add_role(Role('Baker', 'B', 2))
    GlobalRoleList.add_role(Role('Steward', 'S', 9))
    GlobalRoleList.add_role(Role('Fisherman', 'F', 7))

    m = MasterUndoModel()

    app = QtGui.QApplication(sys.argv)
    w = EventWidget(None)

    e = Events.Event(None)
    w.setEvent(e)
    m.add_command_contributer(w)
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()