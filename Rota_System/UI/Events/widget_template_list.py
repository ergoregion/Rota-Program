__author__ = 'Neil Butcher'

from PyQt4 import QtGui, QtCore
import widget_template
from model_template_list import EventsTemplatesModel
from Rota_System.UI.widget_addDel_table import AddDelTableWidget


class EventTemplateWidget(QtGui.QWidget):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QHBoxLayout(self)
        self.list_widget = AddDelTableWidget(self)
        self.layout.addWidget(self.list_widget)
        self.list_widget.objectSelected.connect(self.setEvent)

        self.event_widget = widget_template.EventTemplateWidget(self)
        self.layout.addWidget(self.event_widget)
        self.event_widget.commandIssued.connect(self.emitCommand)
        self.event_widget.criticalCommandIssued.connect(self.emitCriticalCommand)

    def _set_model(self, model):
        self.list_widget.setModel(model)
        model.commandIssued.connect(self.emitCommand)
        model.criticalCommandIssued.connect(self.emitCriticalCommand)

    @QtCore.pyqtSlot(QtCore.QObject)
    def institution(self, institution):
        model = EventsTemplatesModel(institution)
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
from Rota_System import Institution
from Rota_System.UI.model_undo import MasterUndoModel


def main():
    GlobalRoleList.add_role(Role('Baker', 'B', 2))
    GlobalRoleList.add_role(Role('Singer', 'S', 9))
    GlobalRoleList.add_role(Role('Fisherman', 'F', 7))

    m = MasterUndoModel()

    app = QtGui.QApplication(sys.argv)
    w = EventTemplateWidget(None)

    i = Institution.Institution(None)
    w.institution(i)
    m.add_command_contributer(w)
    w.show()

    v = QtGui.QUndoView(None)
    v.setStack(m.undoStack)
    v.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()