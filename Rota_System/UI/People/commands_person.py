__author__ = 'Neil Butcher'

from PyQt4 import QtGui


class CommandChangePerson(QtGui.QUndoCommand):
    def __init__(self, person, key, value):
        super(CommandChangePerson, self).__init__('Changed the ' + key + ' of ' + person.name)
        self.person = person
        self.key = key
        self.value = value
        if key == 'name':
            self.startingValue = person.name
        elif key == 'email':
            self.startingValue = person.email
        elif key == 'address':
            self.startingValue = person.address
        elif key == 'phone':
            self.startingValue = person.phoneNumber

    def redo(self):
        if self.key == 'name':
            self.person.name = self.value
        elif self.key == 'email':
            self.person.email = self.value
        elif self.key == 'address':
            self.person.address = self.value
        elif self.key == 'phone':
            self.person.phoneNumber = self.value

    def undo(self):
        if self.key == 'name':
            self.person.name = self.startingValue
        elif self.key == 'email':
            self.person.email = self.startingValue
        elif self.key == 'address':
            self.person.address = self.startingValue
        elif self.key == 'phone':
            self.person.phoneNumber = self.startingValue


class CommandChangePersonBlacklist(QtGui.QUndoCommand):
    def __init__(self, person, blacklist_bool, date):
        description = 'Changed the blacklist status of ' + person.name + ' on date' + str(date)
        super(CommandChangePersonBlacklist, self).__init__(description)
        self.person = person
        self.blacklist_bool = blacklist_bool
        self.date = date

    def redo(self):
        if self.blacklist_bool:
            self.person.blacklistDate(self.date)
        else:
            self.person.freeDate(self.date)

    def undo(self):
        if self.blacklist_bool:
            self.person.freeDate(self.date)
        else:
            self.person.blacklistDate(self.date)