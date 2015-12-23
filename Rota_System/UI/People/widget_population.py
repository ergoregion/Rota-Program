__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from model_population import PopulationModel
from Rota_System.UI.widget_addDel_list import AddDelListWidget
from widget_person import PersonWidget


class PopulationWidget(QtGui.QWidget):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QHBoxLayout(self)
        self.list_widget = AddDelListWidget(self)
        self.layout.addWidget(self.list_widget)
        self.person_widget = PersonWidget(self)
        self.layout.addWidget(self.person_widget)
        self.list_widget.objectSelected.connect(self.person_widget.person)
        self.person_widget.commandIssued.connect(self.emitCommand)
        self.person_widget.criticalCommandIssued.connect(self.emitCriticalCommand)

    def institution(self, institution):
        model = PopulationModel(institution)
        self.setModel(model)
        return model

    def setModel(self, model):
        self.list_widget.setModel(model)
        model.commandIssued.connect(self.emitCommand)
        model.criticalCommandIssued.connect(self.emitCriticalCommand)

    @QtCore.pyqtSlot(QtGui.QUndoCommand)
    def emitCommand(self, command):
        self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def emitCriticalCommand(self):
        self.criticalCommandIssued.emit()


from Rota_System.UI.model_undo import MasterUndoModel
import sys
from Rota_System.Institution import Institution


def main():
    i = Institution(None)
    model = PopulationModel(i)
    m = MasterUndoModel()

    app = QtGui.QApplication(sys.argv)
    w = PopulationWidget(None)
    m.add_command_contributer(w)
    w.setModel(model)
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
