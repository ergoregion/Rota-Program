__author__ = 'Neil Butcher'

from PyQt4 import QtGui


class CommandChangeEvent(QtGui.QUndoCommand):
    def __init__(self, event, key, value):
        super(CommandChangeEvent, self).__init__('Changed the ' + key + ' of ' + event.name)
        self.event = event
        self.key = key
        self.value = value
        if key == 'name':
            self.startingValue = event.name
        elif key == 'title':
            self.startingValue = event.title
        elif key == 'description':
            self.startingValue = event.description
        elif key == 'notes':
            self.startingValue = event.notes
        elif key == 'time':
            self.startingValue = event.time
        elif key == 'date':
            self.startingValue = event.date

    def redo(self):
        if self.key == 'name':
            self.event.name = self.value
        elif self.key == 'title':
            self.event.title = self.value
        elif self.key == 'description':
            self.event.description = self.value
        elif self.key == 'notes':
            self.event.notes = self.value
        elif self.key == 'time':
            self.event.time = self.value
        elif self.key == 'date':
            self.event.date = self.value

    def undo(self):
        if self.key == 'name':
            self.event.name = self.startingValue
        elif self.key == 'title':
            self.event.title = self.startingValue
        elif self.key == 'description':
            self.event.description = self.startingValue
        elif self.key == 'notes':
            self.event.notes = self.startingValue
        elif self.key == 'time':
            self.event.time = self.startingValue
        elif self.key == 'date':
            self.event.date = self.startingValue