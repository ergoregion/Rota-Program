__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from Rota_System.StandardTimes import date_string


def date(an_event):
    return an_event.date


def name(a_person):
    return a_person.name


class AvailabilityModel(QtCore.QAbstractTableModel):
    """This combines an event model and a population model to simplify the setting of availabilities"""

    def __init__(self, event_model, population_model):
        super(AvailabilityModel, self).__init__(event_model)
        self._set_models(event_model, population_model)

    def _set_models(self, event_model, population_model):
        self._event_model = event_model
        self._event_model.dataChanged.connect(self.refresh)
        for e in self._event_model.events:
            e.timeChanged.connect(self.refresh)
            e.dateChanged.connect(self.refresh)
        self._population_model = population_model
        self._population_model.dataChanged.connect(self.refresh)
        for p in self._population_model.population:
            p.nameChanged.connect(self.refresh)
            p.dataChanged.connect(self._person_data_changed)

    def dates(self):
        return sorted(set(map(date, self._event_model.events)))

    def people(self):
        return self._population_model.population

    def refresh(self):
        self.reset()

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if len(self.people()) > 0:
                    return self.people()[section].name
            elif orientation == QtCore.Qt.Vertical:
                if len(self.dates()) > 0:
                    return date_string(self.dates()[section])

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return ''
        elif role == QtCore.Qt.BackgroundRole:
            if self._available(index):
                return QtGui.QColor(QtCore.Qt.green)
            else:
                return QtGui.QColor(QtCore.Qt.red)

    def rowCount(self, index):
        return len(self.dates())

    def columnCount(self, index):
        return len(self._population_model.population)

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled

    def _available(self, index):
        p = self.people()[index.column()]
        d = self.dates()[index.row()]
        return p.is_available_on_date(d)

    @QtCore.pyqtSlot(QtCore.QObject)
    def _person_data_changed(self, event):
        i = self.people().index(event)
        self.dataChanged.emit(self.index(i, 0), self.index(i, self.rowCount(i)))