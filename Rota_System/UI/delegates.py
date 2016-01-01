__author__ = 'Neil Butcher'
from PyQt4 import QtCore, QtGui
from datetime import datetime


class ComboDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent, itemslist):
        QtGui.QItemDelegate.__init__(self, parent)
        self.itemslist = itemslist
        self.parent = parent

    def createEditor(self, parent, option, index):
        self.editor = QtGui.QComboBox(parent)
        self.editor.addItems(self.itemslist)
        self.editor.setCurrentIndex(0)
        self.editor.installEventFilter(self)

        return self.editor

    def setEditorData(self, editor, index):
        text = index.data(QtCore.Qt.DisplayRole).toString()
        pos = self.editor.findText(text)
        if pos == -1:
            pos = 0
        self.editor.setCurrentIndex(pos)

    def setModelData(self, editor, model, index):
        value = self.editor.currentText()
        model.setData(index, QtCore.QVariant(value))

    def updateEditorGeometry(self, editor, option, index):
        self.editor.setGeometry(option.rect)


class TimeDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent):
        QtGui.QItemDelegate.__init__(self, parent)
        self.parent = parent

    def createEditor(self, parent, option, index):
        self.editor = QtGui.QTimeEdit(parent)
        self.editor.installEventFilter(self)

        return self.editor

    def setEditorData(self, editor, index):
        timestring = index.data(QtCore.Qt.DisplayRole).toString()
        the_time = datetime.strptime(str(timestring), "%H:%M")
        self.editor.setDateTime(the_time)

    def setModelData(self, editor, model, index):
        value = self.editor.time()
        model.setData(index, value.toPyTime())

    def updateEditorGeometry(self, editor, option, index):
        self.editor.setGeometry(option.rect)


class DateDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent):
        QtGui.QItemDelegate.__init__(self, parent)
        self.parent = parent

    def createEditor(self, parent, option, index):
        self.editor = QtGui.QDateEdit(parent)
        self.editor.installEventFilter(self)

        return self.editor

    def setEditorData(self, editor, index):
        datestring = index.data(QtCore.Qt.DisplayRole).toString()
        the_date = datetime.strptime(str(datestring), "%d. %B %Y")
        self.editor.setDateTime(the_date)

    def setModelData(self, editor, model, index):
        value = self.editor.date()
        model.setData(index, value.toPyDate())

    def updateEditorGeometry(self, editor, option, index):
        self.editor.setGeometry(option.rect)


class TextDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent):
        QtGui.QItemDelegate.__init__(self, parent)
        self.parent = parent

    def createEditor(self, parent, option, index):
        self.editor = QtGui.QLineEdit(parent)
        self.editor.installEventFilter(self)

        return self.editor

    def setEditorData(self, editor, index):
        theString = index.data(QtCore.Qt.DisplayRole).toString()
        self.editor.setText(theString)

    def setModelData(self, editor, model, index):
        value = self.editor.text()
        model.setData(index, value)

    def updateEditorGeometry(self, editor, option, index):
        self.editor.setGeometry(option.rect)
