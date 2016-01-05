__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from Rota_System.UI.Availability import AvailabilitySelectionWidget
from Rota_System.UI.Vacancies import VacanciesWidget
from Rota_System.UI.Events import EventWidget


class SingleDurationWidget(QtGui.QWidget):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QVBoxLayout(self)
        self.tabWidget = QtGui.QTabWidget(self)
        self.layout.addWidget(self.tabWidget)

        self.eventsWidget = EventWidget(self)
        self.availabilityWidget = AvailabilitySelectionWidget(self)
        self.vacanciesWidget = VacanciesWidget(self)
        # self.errorsWidget = ErrorCheckingWidget.ErrorCheckingWidget(self)
        # self.reportsWidget = ReportWidget.ReportWidget(self)

        self.tabWidget.addTab(self.eventsWidget, "Events")
        self.addComandContributer(self.eventsWidget)
        self.tabWidget.addTab(self.availabilityWidget, "Availability")
        self.addComandContributer(self.availabilityWidget)
        self.tabWidget.addTab(self.vacanciesWidget, "Vacancies")
        self.addComandContributer(self.vacanciesWidget)
        # self.tabWidget.addTab(self.errorsWidget,"Error Checking")
        # self.tabWidget.addTab(self.reportsWidget,"Reports")

        self._population_model = None

    def setPopulationModel(self, popModel):
        self._population_model = popModel
        self.vacanciesWidget.populationModel(self._population_model)

    def setDuration(self, duration):
        if self._population_model:
            self._event_model = self.eventsWidget.duration(duration)
            self.availabilityWidget.set_models(self._event_model, self._population_model)
            self.vacanciesWidget.eventsModel(self._event_model)

    @QtCore.pyqtSlot(QtGui.QUndoCommand)
    def emitCommand(self, command):
        self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def emitCriticalCommand(self):
        self.criticalCommandIssued.emit()

    def addComandContributer(self, otherModel):
        otherModel.commandIssued.connect(self.emitCommand)
        otherModel.criticalCommandIssued.connect(self.emitCriticalCommand)



import sys
from Rota_System.Roles import Role, GlobalRoleList
from Rota_System.Institution import Institution
from Rota_System.Duration import Duration
from Rota_System.UI.model_undo import MasterUndoModel
from Rota_System.UI.People.model_population import PopulationModel


def main():
    GlobalRoleList.add_role(Role('Baker', 'B', 2))
    GlobalRoleList.add_role(Role('Singer', 'S', 9))
    GlobalRoleList.add_role(Role('Fisherman', 'F', 7))

    m = MasterUndoModel()
    i = Institution(None)
    p = PopulationModel(i)
    d = Duration(i)

    app = QtGui.QApplication(sys.argv)
    w = SingleDurationWidget(None)
    w.setPopulationModel(p)
    w.setDuration(d)

    m.add_command_contributer(w)
    w.show()

    v = QtGui.QUndoView(None)
    v.setStack(m.undoStack)
    v.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()