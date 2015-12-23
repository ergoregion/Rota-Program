__author__ = 'Neil Butcher'

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import pyqtSignal
from Rota_System.Worker import Worker
from datetime import date
import sys
from commands_person import CommandChangePerson, CommandChangePersonBlacklist
from Rota_System.UI.Roles import RoleListWidget
from Rota_System.Roles import Role, GlobalRoleList


class PersonWidget(QtGui.QWidget):
    commandIssued = pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = pyqtSignal()

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi('PersonWidget.ui', self)
        self.roleListWidget = RoleListWidget(self)
        self.roleListStackedWidget.addWidget(self.roleListWidget)
        self._person = None
        self._roleListModel = None

    @QtCore.pyqtSlot(QtCore.QObject)
    def person(self, person):
        if self._roleListModel:
            self._roleListModel.commandIssued.disconnect(self.emitCommand)
        if self._person:
            self._person.dataChanged.disconnect(self.update)
        self._person = person
        person.dataChanged.connect(self.update)
        self._roleListModel = self.roleListWidget.roleList(person._roles)
        self._roleListModel.commandIssued.connect(self.emitCommand)
        self.update()

    @QtCore.pyqtSlot()
    def update(self):
        self.nameBox.setText(self._person.name)
        self.emailBox.setText(self._person.email)
        self.phoneBox.setText(self._person.phoneNumber)
        self._refreshDates()

    def _refreshDates(self):
        self.blacklistedDates.clear()
        for date in self._person.blacklisted_dates():
            self._addBlacklistDateItem(date)

    def _addBlacklistDateItem(self, date):
        newItem = QtGui.QListWidgetItem(str(date), self.blacklistedDates)
        newItem.date = date
        self.blacklistedDates.addItem(newItem)
        return newItem

    @QtCore.pyqtSlot()
    def nameEntered(self):
        string = self.nameBox.text()
        if not string == self._person.name:
            command = CommandChangePerson(self._person, 'name', str(string))
            self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def emailEntered(self):
        string = self.emailBox.text()
        if not string == self._person.email:
            command = CommandChangePerson(self._person, 'email', str(string))
            self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def phoneEntered(self):
        string = self.phoneBox.text()
        if not string == self._person.phoneNumber:
            command = CommandChangePerson(self._person, 'phone', str(string))
            self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def blacklistDate(self):
        date = self.dateEdit.date().toPyDate()
        command = CommandChangePersonBlacklist(self._person, True, date)
        self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def freeDate(self):
        for item in self.blacklistedDates.selectedItems():
            command = CommandChangePersonBlacklist(self._person, False, item.date)
            self.commandIssued.emit(command)

    @QtCore.pyqtSlot(QtGui.QUndoCommand)
    def emitCommand(self, command):
        self.commandIssued.emit(command)


def main():

    GlobalRoleList.add_role(Role('Baker', 'B', 2))
    GlobalRoleList.add_role(Role('Steward', 'S', 9))
    GlobalRoleList.add_role(Role('Fisherman', 'F', 7))
    bob = Worker()
    bob.name = 'Bob'
    bob.email = 'bob@a.com'
    bob.phoneNumber = '0116'
    testdate = date(2012, 12, 31)
    bob.blacklist_date(testdate)
    app = QtGui.QApplication(sys.argv)
    w = PersonWidget(None)
    w.setWindowTitle('Person')
    w.person(bob)
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
