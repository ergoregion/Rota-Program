__author__ = 'Neil Butcher'

from PyQt4 import QtGui

class CommandChangeDuration(QtGui.QUndoCommand):
    def __init__(self, duration, key, value):
        super(QtGui.QUndoCommand, self).__init__('Changed the ' + key +' of a duration')
        self.duration = duration
        self.key = key
        self.value = value
        if key == 'name':
            self.startingValue = duration.name
        elif key == 'description':
            self.startingValue = duration.description


    def redo(self):
        if self.key == 'description':
            self.duration.description = self.value
        elif self.key == 'name':
            self.duration.name = self.value

    def undo(self):
        if self.key == 'description':
            self.duration.description = self.startingValue
        elif self.key == 'name':
            self.duration.name = self.startingValue