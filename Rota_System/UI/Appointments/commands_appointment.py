__author__ = 'Neil Butcher'

from PyQt4 import QtGui


class CommandAppointVacate(QtGui.QUndoCommand):
    def __init__(self, appointment, person):
        if person:
            desc_string = 'Appointed ' + str(person) + ' to an appointment'
        else:
            desc_string = 'Vacated an appointment'
        QtGui.QUndoCommand.__init__(self, desc_string)
        self.appointment = appointment
        self.person = person
        # use person = None to vacate
        self.preAppointed = self.appointment.isFilled()
        if self.preAppointed:
            self.oldPerson = self.appointment.person

    def redo(self):
        self.appointment.vacate()
        if self.person:
            self.appointment.appoint(self.person)

    def undo(self):
        self.appointment.vacate()
        if self.preAppointed:
            self.appointment.appoint(self.oldPerson)


class CommandAppointmentNote(QtGui.QUndoCommand):
    def __init__(self, appointment, note):
        QtGui.QUndoCommand.__init__(self, 'Added a new note to an appointment')
        self.appointment = appointment
        self.note = note
        self.oldNote = appointment.note

    def redo(self):
        self.appointment.note = self.note

    def undo(self):
        self.appointment.note = self.oldNote


class CommandAppointmentDisable(QtGui.QUndoCommand):
    def __init__(self, appointment, to_be_disabled):
        QtGui.QUndoCommand.__init__(self, 'Disabled an appointment')
        self.appointment = appointment
        self.to_be_disabled = to_be_disabled
        self.pre_disabled = appointment.disabled

    def redo(self):
        self.appointment.disabled = self.to_be_disabled

    def undo(self):
        self.appointment.disabled = self.pre_disabled
