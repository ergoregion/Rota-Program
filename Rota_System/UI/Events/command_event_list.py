__author__ = 'Neil Butcher'

from PyQt4 import QtGui


class CommandAddTemplate(QtGui.QUndoCommand):
    def __init__(self, model, row, parent):
        super(CommandAddTemplate, self).__init__('Added a new template')
        self.model = model
        self.row = row
        self.parent = parent
        self.template = model.new_template()

    def redo(self):
        self.model.beginInsertRows(self.parent, self.row, self.row)
        self.model.templates.insert(self.row, self.template)
        self.template.nameChanged.connect(self.model._templateNameChanged)
        self.model.endInsertRows()

    def undo(self):
        self.model.beginRemoveRows(self.parent, self.row, self.row)
        self.model.templates.pop(self.row)
        self.template.nameChanged.disconnect(self.model._templateNameChanged)
        self.model.endRemoveRows()


class CommandRemoveTemplate(QtGui.QUndoCommand):
    def __init__(self, model, row, parent):
        super(CommandRemoveTemplate, self).__init__('Removed a template')
        self.model = model
        self.row = row
        self.parent = parent
        self.template = model.templates[row]

    def undo(self):
        self.model.beginInsertRows(self.parent, self.row, self.row)
        self.model.templates.insert(self.row, self.template)
        self.template.nameChanged.connect(self.model._templateNameChanged)
        self.model.endInsertRows()

    def redo(self):
        self.model.beginRemoveRows(self.parent, self.row, self.row)
        self.model.templates.pop(self.row)
        self.template.nameChanged.disconnect(self.model._templateNameChanged)
        self.model.endRemoveRows()


class CommandAddEvent(QtGui.QUndoCommand):
    def __init__(self, model, row, parent):
        super(CommandAddEvent, self).__init__('Added a new event')
        self.model = model
        self.row = row
        self.parent = parent
        self.event = model.new_event()

    def redo(self):
        self.model.beginInsertRows(self.parent, self.row, self.row)
        self.model.events.insert(self.row, self.event)
        self.event.changed.connect(self.model._eventChanged)
        self.model.endInsertRows()

    def undo(self):
        self.model.beginRemoveRows(self.parent, self.row, self.row)
        self.model.events.pop(self.row)
        self.event.changed.disconnect(self.model._eventChanged)
        self.model.endRemoveRows()


class CommandRemoveEvent(QtGui.QUndoCommand):
    def __init__(self, model, row, parent):
        super(CommandRemoveEvent, self).__init__('Removed a event')
        self.model = model
        self.row = row
        self.parent = parent
        self.event = model.objects(row)

    def undo(self):
        self.model.beginInsertRows(self.parent, self.row, self.row)
        self.model.events.insert(self.row, self.event)
        self.event.changed.connect(self.model._eventChanged)
        self.model.endInsertRows()

    def redo(self):
        self.model.beginRemoveRows(self.parent, self.row, self.row)
        self.model.events.pop(self.row)
        self.event.changed.disconnect(self.model._eventChanged)
        self.model.endRemoveRows()