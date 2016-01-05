__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from model_population_filter import PopulationSortFilterModel
import Filters


class CandidatesWidget(QtGui.QWidget):
    candidateSelected = QtCore.pyqtSignal(QtCore.QObject)

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self._appointment = None
        self.layout = QtGui.QGridLayout(self)

        self.layout.addWidget(QtGui.QLabel('Candidates'), 0, 0, 1, 1)
        self._availableWidget = QtGui.QListView(self)
        self._availableModel = PopulationSortFilterModel(self._availableWidget)
        self._availableWidget.setModel(self._availableModel)
        self.layout.addWidget(self._availableWidget, 1, 0, 2, 1)

        self._availableWidget.clicked.connect(self._available_list_clicked)

        self.layout.addWidget(QtGui.QLabel('Otherwise Occupied'), 0, 1, 1, 1)
        self._qualifiedWidget = QtGui.QListView(self)
        self._qualifiedWidget.setEnabled(False)
        self._qualifiedModel = PopulationSortFilterModel(self._qualifiedWidget)
        self._qualifiedWidget.setModel(self._qualifiedModel)
        self.layout.addWidget(self._qualifiedWidget, 1, 1, 1, 1)

        self._forceButton = QtGui.QPushButton('Force', self)
        self._forceButton.clicked.connect(self._force_button_pushed)
        self.layout.addWidget(self._forceButton, 2, 1, 1, 1)

        self._qualifiedWidget.clicked.connect(self._qualified_list_clicked)

    @QtCore.pyqtSlot(QtCore.QObject)
    def appointment(self, appointment):
        if self._appointment:
            self._appointment.changed.disconnect(self._update)
        self._appointment = appointment
        if self._appointment:
            self._appointment.changed.connect(self._update)
        self._update()

    def _update(self):
        self._update_filters()
        self._qualifiedWidget.setEnabled(False)

    def _update_filters(self):
        if self._appointment is None:
            qualified_filter = Filters.PersonFilterNobody(self._appointment)
            available_filter = Filters.PersonFilterNobody(self._appointment)
            otherwise_occupied_filter = Filters.PersonFilterNobody(self._appointment)
        else:
            qualified_filter = Filters.PersonFilterQualifiedForAppointment(self._appointment)
            available_filter = Filters.PersonFilterAvailableForAppointment(self._appointment)
            otherwise_occupied_filter = Filters.PersonFilterHasClashingAppointmentInEvent(self._appointment)

        self._qualifiedModel.clear_filters()
        self._qualifiedModel.add_filter(qualified_filter)
        self._qualifiedModel.add_filter(available_filter)
        self._qualifiedModel.add_filter(otherwise_occupied_filter)

        self._availableModel.clear_filters()
        self._availableModel.add_filter(qualified_filter)
        self._availableModel.add_filter(available_filter)
        self._availableModel.add_reversed_filter(otherwise_occupied_filter)

    def populationModel(self, population_model):
        self._availableModel.setSourceModel(population_model)
        self._qualifiedModel.setSourceModel(population_model)

    def population(self):
        return self._availableModel.sourceModel().population

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def _available_list_clicked(self, index):
        person = self._availableModel.object(index)
        self.candidateSelected.emit(person)
        self._qualifiedWidget.setEnabled(False)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def _qualified_list_clicked(self, index):
        person = self._qualifiedModel.object(index)
        self.candidateSelected.emit(person)
        self._qualifiedWidget.setEnabled(False)

    @QtCore.pyqtSlot()
    def _force_button_pushed(self):
        self._qualifiedWidget.setEnabled(True)
        timeout_timer = QtCore.QTimer()
        timeout_timer.singleShot(8000, self._force_button_timeout)

    @QtCore.pyqtSlot()
    def _force_button_timeout(self):
        self._qualifiedWidget.setEnabled(False)