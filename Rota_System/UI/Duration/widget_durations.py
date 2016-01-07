__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from widget_duration import SingleDurationWidget
from Rota_System.UI.widget_addDel_combo import AddDelComboWidget


class DurationsWidget(QtGui.QWidget):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QVBoxLayout(self)
        self.comboWidget = AddDelComboWidget(self)
        self.layout.addWidget(self.comboWidget)

        self.singleDurationWidget = SingleDurationWidget(self)
        self.layout.addWidget(self.singleDurationWidget)
        self.addComandContributer(self.singleDurationWidget)

        self.comboWidget.objectSelected.connect(self.singleDurationWidget.setDuration)

    def setPopulationModel(self, model):
        self.singleDurationWidget.setPopulationModel(model)

    def setModel(self, model):
        self.comboWidget.setModel(model)
        if len(model.durations) > 0:
            self.singleDurationWidget.setDuration(model.durations[0])
        self.addComandContributer(model)

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
from model_durations import DurationsModel
from Rota_System.UI.model_undo import MasterUndoModel
from Rota_System.UI.People.model_population import PopulationModel


def main():
    GlobalRoleList.add_role(Role('Baker', 'B', 2))
    GlobalRoleList.add_role(Role('Singer', 'S', 9))
    GlobalRoleList.add_role(Role('Fisherman', 'F', 7))

    m = MasterUndoModel()
    i = Institution(None)
    p = PopulationModel(i)
    d = DurationsModel(i)

    app = QtGui.QApplication(sys.argv)
    w = DurationsWidget(None)
    w.setPopulationModel(p)
    w.setModel(d)

    m.add_command_contributer(w)
    w.show()

    v = QtGui.QUndoView(None)
    v.setStack(m.undoStack)
    v.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()