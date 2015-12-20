__author__ = 'Neil Butcher'

import sys

from PyQt4 import QtCore, QtGui

from commands_role import CommandChangeRole


class SingleRoleWidget(QtGui.QWidget):

    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self._role = None
        self.layout = QtGui.QHBoxLayout(self)
        self.descriptionBox = QtGui.QLineEdit(self)
        self.descriptionBox.editingFinished.connect(self.description_enter)
        self.layout.addWidget(self.descriptionBox)
        self.priorityBox = QtGui.QComboBox(self)
        self.priorityBox.setMaxVisibleItems(10)
        self.priorityBox.addItems(
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        )
        self.priorityBox.activated.connect(self.priority_entered)
        self.layout.addWidget(self.priorityBox)

    def role(self, role):
        if self._role:
            self._role.descriptionChanged.disconnect(self.update)
            self._role.priorityChanged.disconnect(self.update)
        self._role = role
        role.descriptionChanged.connect(self.update)
        role.priorityChanged.connect(self.update)
        self.update()

    def update(self):
        self.priorityBox.setCurrentIndex(self._role.priority)
        self.descriptionBox.setText(self._role.description)

    def description_entered(self, string):
        if self._role:
            command = CommandChangeRole(self._role, 'description', str(string))
            self.commandIssued.emit(command)

    def description_enter(self):
        if self._role:
            string = self.descriptionBox.text()
            if not string == self._role.description:
                command = CommandChangeRole(self._role, 'description', str(string))
                self.commandIssued.emit(command)

    def priority_entered(self, integer):
        if self._role:
            command = CommandChangeRole(self._role, 'priority', integer)
            self.commandIssued.emit(command)


def main():
    app = QtGui.QApplication(sys.argv)
    w = SingleRoleWidget(None)
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()