__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from command_event_list import CommandAddTemplate, CommandRemoveTemplate
from Rota_System.Events import EventPrototype

class EventsTemplatesModel(QtCore.QAbstractListModel):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, institution):
        QtCore.QAbstractItemModel.__init__(self, institution)
        self.institution = institution
        self.templates = institution.templates
        for p in self.templates:
            p.nameChanged.connect(self._templateNameChanged)

    def rowCount(self, parent):
        return len(self.templates)

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != QtCore.Qt.DisplayRole:
            return None
        template = self.templates[index.row()]
        return QtCore.QVariant(template.name)

    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return None
        return None

    def object(self, index):
        return self.templates[index.row()]

    def criticalDelete(self):
        return False

    def insertRow(self, row, parent=QtCore.QModelIndex()):
        command = CommandAddTemplate(self, row, parent)
        self.commandIssued.emit(command)

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        command = CommandRemoveTemplate(self, row, parent)
        self.commandIssued.emit(command)

    def new_template(self):
        return EventPrototype(self.institution)

    @QtCore.pyqtSlot(QtCore.QObject)
    def _templateNameChanged(self, template):
        i = self.templates.index(template)
        index = self.index(i)
        self.dataChanged.emit(index, index)
