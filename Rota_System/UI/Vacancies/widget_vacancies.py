__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from Rota_System.UI.Appointments import SingleAppointmentWidget, AppointmentsTreeListWidget
from Rota_System.UI.Candidating import CandidatesWidget


def autoFill(all_appointments, appointments_to_fill, people):
    pass


class VacanciesWidget(QtGui.QWidget):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QGridLayout(self)
        self.treeWidget = AppointmentsTreeListWidget(self)
        self.treeWidget.showCheckBoxes = True
        self.layout.addWidget(self.treeWidget, 0, 0, 5, 1)

        self.appointmentWidget = SingleAppointmentWidget(self)
        self.appointmentWidget.setFixedHeight(170)
        self.appointmentWidget.setFixedWidth(280)
        self.appointmentWidget.commandIssued.connect(self.emitCommand)
        self.layout.addWidget(self.appointmentWidget, 0, 1, 1, 1)
        self._vacantCandidatesText = QtGui.QLabel('0 appointments are vacant')
        self.layout.addWidget(self._vacantCandidatesText, 1, 1, 1, 1)
        self._selectedCandidatesText = QtGui.QLabel('0 appointments are selected')
        self.layout.addWidget(self._selectedCandidatesText, 2, 1, 1, 1)
        self._vacantSelectedText = QtGui.QLabel('0 appointments are vacant and selected')
        self.layout.addWidget(self._vacantSelectedText, 3, 1, 1, 1)
        self._fillButton = QtGui.QPushButton('Fill these appointments')
        self._fillButton.clicked.connect(self.autofill)
        self.layout.addWidget(self._fillButton, 4, 1, 1, 1)

        self.candidatesWidget = CandidatesWidget(self)
        self.layout.addWidget(self.candidatesWidget, 0, 2, 5, 1)

        self.treeWidget.appointmentSelected.connect(self.appointmentWidget.appointment)
        self.treeWidget.appointmentSelected.connect(self.candidatesWidget.appointment)
        self.treeWidget.checkedChanged.connect(self._updateSelectedAppointmentsText)
        self.treeWidget.vacantAppointmentsChanged.connect(self._updateVacantAppointmentsText)

        self.candidatesWidget.candidateSelected.connect(self.appointmentWidget.appoint)

    def eventsModel(self, eventModel):
        self.treeWidget.eventsModel(eventModel)

    def populationModel(self, populationModel):
        self.candidatesWidget.populationModel(populationModel)

    @QtCore.pyqtSlot(int, int)
    def _updateSelectedAppointmentsText(self, n_selected_items, n_selected_vacant_items):
        self._selectedCandidatesText.setText(str(n_selected_items) + ' appointments are selected')
        self._vacantSelectedText.setText(str(n_selected_vacant_items) + ' appointments are selected and vacant')

    @QtCore.pyqtSlot(int, int)
    def _updateVacantAppointmentsText(self, n_vacant_items, n_selected_vacant_items):
        self._vacantCandidatesText.setText(str(n_vacant_items) + ' appointments are vacant')
        self._vacantSelectedText.setText(str(n_selected_vacant_items) + ' appointments are selected and vacant')

    @QtCore.pyqtSlot()
    def autofill(self):
        people = self.candidatesWidget.population()
        appointments_to_fill = self.treeWidget.checkedVacantAppointments()
        all_appointments = self.treeWidget.appointments()

        autoFill(all_appointments, appointments_to_fill, people)


    @QtCore.pyqtSlot(QtGui.QUndoCommand)
    def emitCommand(self, command):
        self.commandIssued.emit(command)

import sys
from Rota_System.Roles import Role, GlobalRoleList
from Rota_System import Duration
from Rota_System.UI.model_undo import MasterUndoModel


def main():
    GlobalRoleList.add_role(Role('Baker', 'B', 2))
    GlobalRoleList.add_role(Role('Singer', 'S', 9))
    GlobalRoleList.add_role(Role('Fisherman', 'F', 7))

    m = MasterUndoModel()

    app = QtGui.QApplication(sys.argv)
    w = VacanciesWidget(None)

    m.add_command_contributer(w)
    w.show()

    v = QtGui.QUndoView(None)
    v.setStack(m.undoStack)
    v.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()