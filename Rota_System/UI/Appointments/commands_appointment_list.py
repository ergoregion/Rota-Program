__author__ = 'Neil Butcher'

from PyQt4 import QtGui
from Rota_System import Appointments


class CommandAddAppointment(QtGui.QUndoCommand):
    def __init__(self, model, row, parent):
        QtGui.QUndoCommand.__init__(self, 'Added a new appointment')
        self.model = model
        self.event = self.model.event
        self.row = row
        self.parent = parent
        if self.model.event.template:
            self.appointment = Appointments.AppointmentPrototype(self.model.event, self.model.currentRole)
        else:
            self.appointment = Appointments.Appointment(self.model.event, self.model.currentRole, self.model.event)

    def redo(self):
        self.model.beginInsertRows(self.parent, self.row, self.row)
        self.event.add_appointment(self.appointment)
        self.model.endInsertRows()

    def undo(self):
        self.model.beginRemoveRows(self.parent, self.row, self.row)
        self.event.remove_appointment(self.appointment)
        self.model.endRemoveRows()
        self.model.reset()


class CommandRemoveAppointment(QtGui.QUndoCommand):
    def __init__(self, model, row, parent):
        QtGui.QUndoCommand.__init__(self, 'Removed an appointment')
        self.model = model
        self.event = self.model.event
        self.row = row
        self.parent = parent
        self.appointment = self.model.event.appointments[row]

    def redo(self):
        self.model.beginRemoveRows(self.parent, self.row, self.row)
        self.event.remove_appointment(self.appointment)
        self.model.endRemoveRows()
        self.model.reset()

    def undo(self):
        self.model.beginInsertRows(self.parent, self.row, self.row)
        self.event.add_appointment(self.appointment)
        self.model.endInsertRows()
