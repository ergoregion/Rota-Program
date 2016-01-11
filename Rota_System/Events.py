__author__ = 'Neil Butcher'

from PyQt4.QtCore import pyqtSignal, QObject
from datetime import time, date, datetime
from Appointments import Appointment, AppointmentPrototype


class EventAbstract(QObject):
    titleChanged = pyqtSignal(str)
    changed = pyqtSignal(QObject)
    timeChanged = pyqtSignal()
    appointmentsChanged = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        self._title = ''
        self._notes = ''
        self._description = ''
        self.appointments = []
        self.template = False

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.titleChanged.emit(value)
        self.changed.emit(self)

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = value
        self.changed.emit(self)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value
        self.changed.emit(self)

    def add_appointment(self, appointment):
        self.appointments.append(appointment)
        self.appointmentsChanged.emit()

    def remove_appointment(self, appointment):
        self.appointments.remove(appointment)
        self.appointmentsChanged.emit()


class EventPrototype(EventAbstract):
    nameChanged = pyqtSignal(QObject)

    def __init__(self, parent):
        EventAbstract.__init__(self, parent)
        self._time = time(9, 0, 0)
        self._name = 'New Template'
        self.template = True

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.nameChanged.emit(self)
        self.changed.emit(self)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        self.changed.emit(self)
        self.timeChanged.emit()

    def add_appointment(self, appointment):
        assert isinstance(appointment, AppointmentPrototype)
        EventAbstract.add_appointment(self, appointment)

    def create_event(self, a_date=date(2000, 01, 01), parent=None):

        if parent:
            e = Event(parent)
        else:
            e = Event(self.parent())
        e._title = self._title
        e._datetime = datetime.combine(a_date, self._time)
        e._notes = self._notes
        e._description = self._description
        e._appointments = []
        for a in self.appointments:
            new_appointment = a.create_in(e)
            e.appointments.append(new_appointment)
        return e


class Event(EventAbstract):
    dateChanged = pyqtSignal()

    def __init__(self, parent):
        EventAbstract.__init__(self, parent)
        self._datetime = datetime(2000,1,1,0,0,0)

    @property
    def name(self):
        return self._title

    @property
    def date(self):
        return self._datetime.date()

    @date.setter
    def date(self, value):
        new_date_time = datetime.combine(value, self._datetime.time())
        self._datetime = new_date_time
        self.changed.emit(self)
        self.dateChanged.emit()

    @property
    def time(self):
        return self._datetime.time()

    @time.setter
    def time(self, value):
        new_date_time = datetime.combine(self._datetime.date(), value)
        self._datetime = new_date_time
        self.changed.emit(self)
        self.timeChanged.emit()

    def datetime(self):
        return self._datetime

    def add_appointment(self, appointment):
        assert isinstance(appointment, Appointment)
        EventAbstract.add_appointment(self, appointment)