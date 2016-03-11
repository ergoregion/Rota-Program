__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui


class LoadSaveBarWidget(QtGui.QWidget):

    save = QtCore.pyqtSignal()
    load = QtCore.pyqtSignal()
    export_excell = QtCore.pyqtSignal()
    import_excell = QtCore.pyqtSignal()

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

        self.layout = QtGui.QHBoxLayout(self)

        self.savePushButton = QtGui.QPushButton('Save', self)
        self.savePushButton.clicked.connect(self._save)
        self.layout.addWidget(self.savePushButton)

        self.loadPushButton = QtGui.QPushButton('Load', self)
        self.loadPushButton.clicked.connect(self._load)
        self.layout.addWidget(self.loadPushButton)

        self.exportPushButton = QtGui.QPushButton('Export Excell', self)
        self.exportPushButton.clicked.connect(self._export)
        self.layout.addWidget(self.exportPushButton)

        self.importPushButton = QtGui.QPushButton('Import Excell', self)
        self.importPushButton.clicked.connect(self._import)
        self.layout.addWidget(self.importPushButton)

    @QtCore.pyqtSlot()
    def _save(self):
        self.save.emit()

    @QtCore.pyqtSlot()
    def _load(self):
        self.load.emit()

    @QtCore.pyqtSlot()
    def _export(self):
        self.export_excell.emit()

    @QtCore.pyqtSlot()
    def _import(self):
        self.import_excell.emit()