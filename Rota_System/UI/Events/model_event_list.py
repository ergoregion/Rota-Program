__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from command_event_list import CommandAddEvent, CommandRemoveEvent
from command_event import CommandChangeEvent
from Rota_System.Events import Event


class EventsModel(QtCore.QAbstractTableModel):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, duration):
        super(EventsModel, self).__init__(duration)
        self.duration = duration
        self.events = duration.events
        for p in self.events:
            p.changed.connect(self._eventChanged)

    def rowCount(self, index):
        return len(self.events)

    def columnCount(self, index):
        return 2

    def object(self, index):
        return self.events[index.row()]

    def objects(self, row):
        return self.events[row]

    def criticalDelete(self):
        return True

    def flags(self, index):
        if index.column() == 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        item = self.events[index.row()]

        if role != QtCore.Qt.DisplayRole:
            return None

        if index.column() == 0:
            return QtCore.QVariant(item.name)
        elif index.column() == 1:
            return QtCore.QVariant(item.date.strftime("%d. %B %Y"))
        else:
            return QtCore.QVariant()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return None
        if role != QtCore.Qt.EditRole:
            return None

        if value == self.events[index.row()].date:
            return True
        item = self.events[index.row()]
        command = CommandChangeEvent(item, 'date', value)
        self.commandIssued.emit(command)
        return True

    def insertRow(self, row, parent=QtCore.QModelIndex()):
        command = CommandAddEvent(self, row, parent)
        self.commandIssued.emit(command)

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        command = CommandRemoveEvent(self, row, parent)
        self.commandIssued.emit(command)

    def new_event(self):
        if self.duration.institution is None:
            return Event(parent=self.duration)
        template_name_list = map(str, self.duration.institution.templates)
        if len(template_name_list) == 0:
            return Event(parent=self.duration)
        templateName, ok = QtGui.QInputDialog.getItem(None, "SelectTemplate",
                                                      "Template:", template_name_list, 0, False)
        if ok:
            index = template_name_list.index(templateName)
            return self.duration.institution.templates[index].create_event(parent=self.duration)
        else:
            return Event(parent=self.duration)

    def headerData(self, section, orientation, role):
        return None

    @QtCore.pyqtSlot(QtCore.QObject)
    def _eventChanged(self, event):
        i = self.events.index(event)
        index1 = self.index(i, 0)
        index2 = self.index(i, 1)
        self.dataChanged.emit(index1, index2)
