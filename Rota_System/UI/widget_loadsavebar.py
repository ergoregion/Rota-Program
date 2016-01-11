__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui


class LoadSaveBarWidget(QtGui.QWidget):

    save = QtCore.pyqtSignal()
    load = QtCore.pyqtSignal()

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

        self.layout = QtGui.QHBoxLayout(self)

        self.savePushButton = QtGui.QPushButton('Save', self)
        self.savePushButton.clicked.connect(self._save)
        self.layout.addWidget(self.savePushButton)

        self.loadPushButton = QtGui.QPushButton('Load', self)
        self.loadPushButton.clicked.connect(self._load)
        self.layout.addWidget(self.loadPushButton)

    @QtCore.pyqtSlot()
    def _save(self):
        self.save.emit()

    @QtCore.pyqtSlot()
    def _load(self):
        self.load.emit()