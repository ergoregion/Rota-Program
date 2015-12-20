__author__ = 'Neil Butcher'


from PyQt4 import QtGui
from Rota_System.Roles import Role


class CommandAddRole(QtGui.QUndoCommand):
    def __init__(self, model, row, parent):
        super(CommandAddRole, self).__init__('Added a new role')
        self.model = model
        self.row = row
        self.parent = parent
        self.role = Role('A new Role', self.model.rolelist.new_code(), 0)

    def redo(self):
        self.model.beginInsertRows(self.parent, self.row, self.row)
        self.model.aboutToAddRole.emit()
        for _ in range(1):
            self.model.rolelist.addRole(self.role)
        self.model.endInsertRows()
        self.model.addRole.emit()

    def undo(self):
        self.model.aboutToRemoveRole.emit(self.role.code)
        self.model.beginRemoveRows(self.parent, self.row, self.row)
        for _ in range(1):
            self.model.rolelist.removeRole(self.role)
        self.model.endRemoveRows()
        self.model.removeRole.emit(self.role.code)