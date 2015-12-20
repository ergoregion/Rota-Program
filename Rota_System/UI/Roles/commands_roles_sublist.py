__author__ = 'Neil Butcher'

from PyQt4 import QtGui


class CommandIncludeRole(QtGui.QUndoCommand):
    def __init__(self, role_list_selection, role):
        super(CommandIncludeRole, self).__init__('Added a new role')
        self.role_list_selection = role_list_selection
        self._role = role

    def redo(self):
        self.role_list_selection.addFromCode(self._role.code)

    def undo(self):
        self.role_list_selection.removeFromCode(self._role.code)


class CommandExcludeRole(QtGui.QUndoCommand):
    def __init__(self, role_list_selection, role):
        super(CommandExcludeRole, self).__init__('Removed a role')
        self.role_list_selection = role_list_selection
        self._role = role

    def undo(self):
        self.role_list_selection.addFromCode(self._role.code)

    def redo(self):
        self.role_list_selection.removeFromCode(self._role.code)