__author__ = 'Neil Butcher'

from PyQt4 import QtGui


class CommandChangeRole(QtGui.QUndoCommand):
    def __init__(self, role, key, value, *__args):
        QtGui.QUndoCommand.__init__(self, *__args)
        self.role = role
        self.key = key
        self.setText('Changed the ' + key + ' of a role')
        self.value = value
        if key == 'description':
            self.startingValue = role.description
        elif key == 'priority':
            self.startingValue = role.priority

    def redo(self):
        if self.key == 'description':
            self.role.description = self.value
        elif self.key == 'priority':
            self.role.priority = self.value

    def undo(self):
        if self.key == 'description':
            self.role.description = self.startingValue
        elif self.key == 'priority':
            self.role.priority = self.startingValue