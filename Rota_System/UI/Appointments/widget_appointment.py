__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui, uic
from commands_appointment import CommandAppointmentDisable, CommandAppointmentNote, CommandAppointVacate
from Rota_System.StandardTimes import date_string
import os


class SingleAppointmentWidget(QtGui.QWidget):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        fn = os.path.join(os.path.dirname(__file__),'AppointmentWidget.ui')
        uic.loadUi(fn, self)
        self._appointment = None

    @QtCore.pyqtSlot(QtCore.QObject)
    def appointment(self, appointment):
        if self._appointment:
            self._appointment.changed.disconnect(self._update)
        self._appointment = appointment
        if self._appointment:
            self._appointment.changed.connect(self._update)
        self._update()

    def _update(self):
        if self._appointment is None:
            self.descriptionBox.setText('No Appointment Selected')
            self.notesBox.setText('')
            self.checkBox.setChecked(True)
        else:
            self.descriptionBox.setText(
                str(self._appointment.role) + '(' + self._appointment.event.title + ')' + '(' + date_string(
                    self._appointment.date) + ')')
            self.notesBox.setText(self._appointment.note)
            self.checkBox.setChecked(self._appointment.disabled)

        if self._appointment is None:
            self.personLine.setText('')
            self.vacateButton.setEnabled(False)
        elif self._appointment.disabled:
            self.personLine.setText('***Disabled***')
            self.vacateButton.setEnabled(False)
        elif self._appointment.is_filled():
            self.personLine.setText(str(self._appointment.person))
            self.vacateButton.setEnabled(True)
        else:
            self.personLine.setText('***Vacant***')
            self.vacateButton.setEnabled(False)

    @QtCore.pyqtSlot()
    def changedNote(self):
        if self._appointment:
            command = CommandAppointmentNote(self._appointment, str(self.notesBox.text()))
            self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def vacate(self):
        self.appoint(None)

    @QtCore.pyqtSlot(bool)
    def disableAppointment(self, disable):
        if self._appointment:
            if self._appointment.disabled is not disable:
                command = CommandAppointmentDisable(self._appointment, disable)
                self.commandIssued.emit(command)

    @QtCore.pyqtSlot(QtCore.QObject)
    def appoint(self, person):
        if self._appointment:
            command = CommandAppointVacate(self._appointment, person)
            self.commandIssued.emit(command)


import sys
from Rota_System.Appointments import Appointment
from Rota_System import Roles, Events


def main():

    Roles.GlobalRoleList.add_role(Roles.Role('Baker', 'B', 10))
    r = Roles.role('B')
    e = Events.Event(None)
    a = Appointment(e, r, e)
    app = QtGui.QApplication(sys.argv)
    w = SingleAppointmentWidget(None)
    w.appointment(a)
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
