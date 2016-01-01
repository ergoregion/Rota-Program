__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from Roles import GlobalRolesWidget
from People import PopulationWidget
from StandardTimes import StandardEventTimesWidget
from Events import EventTemplateWidget


class InstitutionCoreWidget(QtGui.QWidget):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QVBoxLayout(self)
        self._tab_widget = QtGui.QTabWidget(self)
        self.layout.addWidget(self._tab_widget)

        self.roles_widget = GlobalRolesWidget(self)
        self._tab_widget.addTab(self.roles_widget, "Roles")
        self._add_command_contributer(self.roles_widget)

        self.population_widget = PopulationWidget(self)
        self._tab_widget.addTab(self.population_widget, "Population")
        self._add_command_contributer(self.population_widget)

        self.times_widget = StandardEventTimesWidget(self)
        self._tab_widget.addTab(self.times_widget, "Named Times")
        self._add_command_contributer(self.times_widget)

        self.template_widget = EventTemplateWidget(self)
        self._tab_widget.addTab(self.template_widget, "Event Templates")
        self._add_command_contributer(self.template_widget)

    def institution(self, institution):
        self.roles_widget.institution(institution)
        self.population_widget.institution(institution)
        self.times_widget.institution(institution)
        self.template_widget.institution(institution)

    @QtCore.pyqtSlot(QtGui.QUndoCommand)
    def emitCommand(self, command):
        self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def emitCriticalCommand(self):
        self.criticalCommandIssued.emit()

    def _add_command_contributer(self, other_model):
        other_model.commandIssued.connect(self.emitCommand)
        other_model.criticalCommandIssued.connect(self.emitCriticalCommand)

import sys
from Rota_System.Roles import GlobalRoleList, Role
from model_undo import MasterUndoModel
from Rota_System.Institution import Institution


def main():
    GlobalRoleList.add_role(Role('Baker', 'B', 2))
    GlobalRoleList.add_role(Role('Singer', 'S', 9))
    GlobalRoleList.add_role(Role('Fisherman', 'F', 7))

    m = MasterUndoModel()

    app = QtGui.QApplication(sys.argv)
    w = InstitutionCoreWidget(None)

    i = Institution(None)
    w.institution(i)
    m.add_command_contributer(w)
    w.show()

    v = QtGui.QUndoView(None)
    v.setStack(m.undoStack)
    v.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()