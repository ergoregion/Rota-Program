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
        self.layout = QtGui.QHBoxLayout(self)
        self.treeWidget = AppointmentsTreeListWidget(self)
        self.treeWidget.showCheckBoxes = True
        self.layout.addWidget(self.treeWidget)

        self.appointmentWidget = SingleAppointmentWidget(self)
        self.appointmentWidget.setFixedHeight(170)
        self.appointmentWidget.setFixedWidth(280)
        self.appointmentWidget.commandIssued.connect(self.commandIssued)
        self._midLayout = QtGui.QVBoxLayout(self)
        self._midLayout.addWidget(self.appointmentWidget)
        self._vacantCandidatesText = QtGui.QLabel('0 appointments are vacant')
        self._midLayout.addWidget(self._vacantCandidatesText)
        self._selectedCandidatesText = QtGui.QLabel('0 appointments are selected')
        self._midLayout.addWidget(self._selectedCandidatesText)
        self._vacantSelectedText = QtGui.QLabel('0 appointments are vacant and selected')
        self._midLayout.addWidget(self._vacantSelectedText)
        self._fillButton = QtGui.QPushButton('Fill these appointments')
        self._fillButton.clicked.connect(self.autofill)
        self._midLayout.addWidget(self._fillButton)
        self.layout.addLayout(self._midLayout)

        self.candidatesWidget = CandidatesWidget(self)
        self.layout.addWidget(self.candidatesWidget)

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
    def _updateSelectedAppointmentsText(self, numberOFSelectedItems, numberOfSelectedVacantItems):
        self._selectedCandidatesText.setText(str(numberOFSelectedItems) + ' appointments are selected')
        self._vacantSelectedText.setText(str(numberOfSelectedVacantItems) + ' appointments are selected and vacant')

    @QtCore.pyqtSlot(int, int)
    def _updateVacantAppointmentsText(self, numberOFVacantItems, numberOfSelectedVacantItems):
        self._vacantCandidatesText.setText(str(numberOFVacantItems) + ' appointments are vacant')
        self._vacantSelectedText.setText(str(numberOfSelectedVacantItems) + ' appointments are selected and vacant')

    @QtCore.pyqtSlot()
    def autofill(self):
        people = self.candidatesWidget.population()
        appointments_to_fill = self.treeWidget.checkedVacantAppointments()
        all_appointments = self.treeWidget.appointments()

        autoFill(all_appointments, appointments_to_fill, people)



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