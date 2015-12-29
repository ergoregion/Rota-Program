__author__ = 'Neil Butcher'

from PyQt4.QtCore import pyqtSignal, QObject


def date(an_event):
    return an_event.date


class Duration(QObject):
    nameChanged = pyqtSignal(QObject)

    def __init__(self, parent):
        QObject.__init__(self, parent)
        self.events = []
        self._name = 'new duration'
        self.institution = parent

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.nameChanged.emit(self)

    def dates(self):
        return sorted(set(map(date, self.events)))

    def appointments(self):
        result = []
        for e in self.events:
            result.extend(e.appointments)
        return result