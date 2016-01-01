__author__ = 'Neil Butcher'

from PyQt4 import QtGui, QtCore, uic
from command_event import CommandChangeEvent
import os


class AbstractEventWidget(QtGui.QWidget):
    commandIssued = QtCore.pyqtSignal(QtGui.QUndoCommand)
    criticalCommandIssued = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.event = None

    @QtCore.pyqtSlot(QtCore.QObject)
    def setEvent(self, item):
        if self.event:
            self.event.changed.disconnect(self.refresh)
        self.event = item
        self.event.changed.connect(self.refresh)
        self.refresh()

    def refresh(self):
        self.titleLineEdit.setText(self.event.title)
        self.notesLineEdit.setText(self.event.notes)
        self.descriptionLineEdit.setText(self.event.description)
        self.timeEdit.setTime(self.event.time)

    @QtCore.pyqtSlot()
    def titleEntered(self):
        string = self.titleLineEdit.text()
        if not string == self.event.title:
            command = CommandChangeEvent(self.event, 'title', str(string))
            self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def notesEntered(self):
        string = self.notesLineEdit.text()
        if not string == self.event.notes:
            command = CommandChangeEvent(self.event, 'notes', str(string))
            self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def descriptionEntered(self):
        string = self.descriptionLineEdit.text()
        if not string == self.event.description:
            command = CommandChangeEvent(self.event, 'description', str(string))
            self.commandIssued.emit(command)

    @QtCore.pyqtSlot(QtCore.QTime)
    def timeEntered(self, qtime):
        t = qtime.toPyTime()
        if not t == self.event.time:
            command = CommandChangeEvent(self.event, 'time', t)
            self.commandIssued.emit(command)

    @QtCore.pyqtSlot(QtGui.QUndoCommand)
    def emitCommand(self, command):
        self.commandIssued.emit(command)

    @QtCore.pyqtSlot()
    def emitCriticalCommand(self):
        self.criticalCommandIssued.emit()


class EventTemplateWidget(AbstractEventWidget):
    def __init__(self, parent=None):
        AbstractEventWidget.__init__(self, parent)
        fn = os.path.join(os.path.dirname(__file__),'EventTemplateWidget.ui')
        uic.loadUi(fn, self)


    def refresh(self):
        AbstractEventWidget.refresh(self)
        self.nameLineEdit.setText(self.event.name)

    @QtCore.pyqtSlot()
    def templateNameEntered(self):
        if not self.event:
            return None
        string = self.nameLineEdit.text()
        if not string == self.event.name:
            command = CommandChangeEvent(self.event, 'name', str(string))
            self.commandIssued.emit(command)


class EventWidget(AbstractEventWidget):
    def __init__(self, parent=None):
        AbstractEventWidget.__init__(self, parent)
        fn = os.path.join(os.path.dirname(__file__),'EventWidget.ui')
        uic.loadUi(fn, self)

    def refresh(self):
        AbstractEventWidget.refresh(self)
        self.dateEdit.setDate(self.event.date)

    @QtCore.pyqtSlot(QtCore.QDate)
    def dateEntered(self, qdate):
        d = qdate.toPyDate()
        if not d == self.event.date:
            command = CommandChangeEvent(self.event, 'date', d)
            self.commandIssued.emit(command)