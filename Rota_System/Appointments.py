__author__ = 'Neil Butcher'

from PyQt4.QtCore import pyqtSignal, QObject


class AppointmentAbstract(QObject):
    changed = pyqtSignal()

    def __init__(self, parent, role):
        QObject.__init__(self, parent)
        self.role = role
        self._note = ''
        self._disabled = False

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, value):
        self._note = value
        self.changed.emit()

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        if value:
            self.vacate()
        self._disabled = value
        self.changed.emit()


class Appointment(AppointmentAbstract):
    vacated = pyqtSignal()
    filled = pyqtSignal(QObject)

    def __init__(self, parent, role, event):
        AppointmentAbstract.__init__(self, parent, role)
        self._event = event
        self._person = None

    @property
    def event(self):
        return self._event

    @property
    def date(self):
        return self._event.date

    @property
    def time(self):
        return self._event.time

    def datetime(self):
        return self._event.datetime()

    @property
    def person(self):
        return self._person

    def vacate(self):
        if self._person is None:
            return self
        self._person = None
        self.vacated.emit()
        self.changed.emit()

    def appoint(self, person):
        self._person = person
        self.filled.emit(person)
        self.changed.emit()

    def is_filled(self):
        return self._person is not None


class AppointmentPrototype(AppointmentAbstract):

    def __init__(self, parent, role):
        AppointmentAbstract.__init__(self, parent, role)

    def create_in(self, event):
        a = Appointment(event, self.role, event)
        a.note = self.note
        a.disabled = self.disabled
        return a

    def vacate(self):
        pass

    def is_filled(self):
        return False