__author__ = "Neil Butcher"

from PyQt4 import QtGui, QtCore
import widget_event
from model_event_list import EventsModel
from Rota_System.UI.widget_addDel_table import AddDelTableWidget
from Rota_System.UI.delegates import DateDelegate


class EventWidget(QtGui.QWidget):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QHBoxLayout(self)
        self.list_widget = AddDelTableWidget(self)
        self.layout.addWidget(self.list_widget)
        self.list_widget.objectSelected.connect(self.setEvent)

        self.list_widget.setItemDelegateForColumn(1, DateDelegate(self))

        self.event_widget = widget_event.EventWidget(self)
        self.layout.addWidget(self.event_widget)
        self.event_widget.commandIssued.connect(self.emitCommand)
        self.event_widget.criticalCommandIssued.connect(self.emitCriticalCommand)

    def _set_model(self, model):
        self.list_widget.setModel(model)
        model.commandIssued.connect(self.emitCommand)
        model.criticalCommandIssued.connect(self.emitCriticalCommand)

    @QtCore.pyqtSlot(QtCore.QObject)
    def duration(self, duration):
        model = EventsModel(duration)
        self._set_model(model)
        return model

    @QtCore.pyqtSlot(QtCore.QObject)
    def setEvent(self, item):
        self.event_widget.setEvent(item)

    @QtCore.pyqtSlot(QtGui.QUndoCommand)
    def emitCommand(self, command):
        self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def emitCriticalCommand(self):
        self.criticalCommandIssued.emit()


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
    w = EventWidget(None)

    d = Duration.Duration(None)
    w.duration(d)
    m.add_command_contributer(w)
    w.show()

    v = QtGui.QUndoView(None)
    v.setStack(m.undoStack)
    v.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()