__author__ = 'Neil Butcher'

from PyQt4 import QtGui


class CommandChangeCompatibilityRole(QtGui.QUndoCommand):
    def __init__(self, role1, role2, setting, *__args):
        QtGui.QUndoCommand.__init__(self, *__args)
        self.setText('Changed the compatibility of roles')
        self.role1 = role1
        self.role2 = role2
        self.setting = setting

    def redo(self):
        if self.setting:
            self.role1.compatibilities.add(self.role2)
            self.role2.compatibilities.add(self.role1)
        else:
            self.role1.compatibilities.remove(self.role2)
            self.role2.compatibilities.remove(self.role1)

    def undo(self):
        if not self.setting:
            self.role1.compatibilities.add(self.role2)
            self.role2.compatibilities.add(self.role1)
        else:
            self.role1.compatibilities.remove(self.role2)
            self.role2.compatibilities.remove(self.role1)
