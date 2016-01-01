__author__ = 'Neil Butcher'

from PyQt4 import QtGui, QtCore
from Rota_System.UI.widget_addDel_table import AddDelTableWidget
from model_times import StandardEventTimesModel
from Rota_System.UI.delegates import TimeDelegate


class StandardEventTimesWidget(QtGui.QWidget):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QVBoxLayout(self)
        self.tableWidget = AddDelTableWidget(self)
        self.layout.addWidget(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(1, TimeDelegate(self))
        self.setModel(StandardEventTimesModel(self))

    def institution(self, i):
        self.tableWidget.update()

    def setModel(self, model):
        self.tableWidget.setModel(model)
        model.commandIssued.connect(self.emitCommand)
        model.criticalCommandIssued.connect(self.emitCriticalCommand)

    @QtCore.pyqtSlot(QtGui.QUndoCommand)
    def emitCommand(self, command):
        self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def emitCriticalCommand(self):
        self.criticalCommandIssued.emit()


import sys
from Rota_System.UI.model_undo import MasterUndoModel


def main():

    m = MasterUndoModel()

    app = QtGui.QApplication(sys.argv)
    w = StandardEventTimesWidget(None)

    m.add_command_contributer(w)
    w.show()

    v = QtGui.QUndoView(None)
    v.setStack(m.undoStack)
    v.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()