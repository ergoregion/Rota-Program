__author__ = 'Neil Butcher'

from PyQt4 import QtGui


class CommandChangePersonBlacklist(QtGui.QUndoCommand):
    def __init__(self, person, blacklist_bool, date):
        description = 'Changed the blacklist status of ' + person.name + ' on date' + str(date)
        super(CommandChangePersonBlacklist, self).__init__(description)
        self.person = person
        self.blacklist_bool = blacklist_bool
        self.date = date

    def redo(self):
        if self.blacklist_bool:
            self.person.blacklist_date(self.date)
        else:
            self.person.free_date(self.date)

    def undo(self):
        if self.blacklist_bool:
            self.person.free_date(self.date)
        else:
            self.person.blacklist_date(self.date)