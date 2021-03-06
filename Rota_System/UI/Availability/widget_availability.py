__author__ = 'Neil Butcher'

from PyQt4 import QtGui, QtCore
from command_availability import CommandChangePersonBlacklist
from model_availability import AvailabilityModel
from Rota_System.Person import Person


class AvailabilitySelectionWidget(QtGui.QWidget):

    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QVBoxLayout(self)
        self.table_widget = QtGui.QTableView(self)
        self.layout.addWidget(self.table_widget)
        self._model = None

    def set_models(self, event_model, population_model):
        new_model = AvailabilityModel(event_model, population_model)
        self._set_model(new_model)

    def _set_model(self, new_model):
        if self._model:
            self.table_widget.clicked.disconnect(self._availability_change)
            self._model.deleteLater()
        self.table_widget.setModel(new_model)
        self.table_widget.clicked.connect(self._availability_change)
        self._model = new_model

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def _availability_change(self, index):
        p = self._model.people()[index.column()]
        d = self._model.dates()[index.row()]
        assert isinstance(p, Person)
        currently_available = p.is_available_on_date(d)
        become_blacklisted = currently_available
        command = CommandChangePersonBlacklist(p, become_blacklisted, d)
        self.commandIssued.emit(command)