__author__ = 'Neil Butcher'

from PyQt4 import QtGui, QtCore
from Rota_System.Roles import GlobalRoleList
from commands_appointment import CommandAppointmentDisable, CommandAppointmentNote
from commands_appointment_list import CommandAddAppointment, CommandRemoveAppointment


class AppointmentsTableModel(QtCore.QAbstractTableModel):
    """
    used to manipulate The appointments of an event
    """

    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.event = None
        self.currentRole = None
        GlobalRoleList.rolesChanged.connect(self._refreshCurrentRole)
        self.show_all_roles = True

    @QtCore.pyqtSlot()
    def _refreshCurrentRole(self):
        if len(GlobalRoleList.roles) > 0:
            self.currentRole = GlobalRoleList.roles[0]
        else:
            self.currentRole = None

    def setEvent(self, new_event):
        if self.event:
            self.event.appointmentsChanged.disconnect(self.reset)
        self.event = new_event
        new_event.appointmentsChanged.connect(self.reset)
        self.reset()

    def roleSelected(self, role):
        self.currentRole = role

    def columnCount(self, index):
        return 3

    def flags(self, index):
        if index.column() == 2:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable
        if index.column() == 1:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def rowCount(self, index):
        if not self.event:
            return 0
        return len(self.event.appointments)

    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation != QtCore.Qt.Horizontal:
            return None
        if section == 0:
            return QtCore.QVariant("role")
        elif section == 1:
            return QtCore.QVariant("notes")
        elif section == 2:
            return QtCore.QVariant("disable")
        else:
            return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        appointment = self.event.appointments[index.row()]
        if index.column() == 2 and role == QtCore.Qt.CheckStateRole:
            return appointment.disabled
        if role != QtCore.Qt.DisplayRole:
            return None
        if index.column() == 0:
            return QtCore.QVariant(str(appointment.role))
        elif index.column() == 1:
            return QtCore.QVariant(str(appointment.note))
        else:
            return QtCore.QVariant()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return None

        appointment = self.event.appointments[index.row()]

        if index.column() == 2 and role == QtCore.Qt.CheckStateRole:
            command = CommandAppointmentDisable(appointment, not self.data(index, role))
            self.commandIssued.emit(command)
            return True

        if role != QtCore.Qt.EditRole:
            return None

        if index.column() == 1:
            command = CommandAppointmentNote(appointment, str(value.toString()))
            self.commandIssued.emit(command)
            return True
        else:
            return None

    def criticalDelete(self):
        return False

    def insertRow(self, row, parent=QtCore.QModelIndex()):
        if self.event:
            command = CommandAddAppointment(self, row, parent)
            self.commandIssued.emit(command)

    def object(self, index):
        return self.event.appointments[index.row()]

    def objects(self):
        return self.event.appointments

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        if self.event:
            command = CommandRemoveAppointment(self, row, parent)
            self.commandIssued.emit(command)
