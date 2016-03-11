__author__ = 'Neil Butcher'

from PyQt4 import QtGui, QtCore
from widget_core import InstitutionCoreWidget
from widget_undobar import UndoBarWidget
from widget_loadsavebar import LoadSaveBarWidget
from Duration import DurationsWidget
from Rota_System.Saving.Database import InstitutionSavingObject
from Rota_System.Saving.Excell import PopulationSavingObject, DurationSavingObject


class InstitutionWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.layout = QtGui.QGridLayout(self)

        self.undoBar = UndoBarWidget(self)
        self.model = self.undoBar.model
        self.layout.addWidget(self.undoBar, 0, 1, 1, 2)

        self.saveBar = LoadSaveBarWidget(self)
        self.layout.addWidget(self.saveBar, 0, 5, 1, 2)
        self.saveBar.load.connect(self.load)
        self.saveBar.save.connect(self.save)
        self.saveBar.import_excell.connect(self.import_excell)
        self.saveBar.export_excell.connect(self.export_excell)

        self.stack_widget = QtGui.QTabWidget(self)
        self.layout.addWidget(self.stack_widget, 1, 0, 1, 8)

        self.core_widget = InstitutionCoreWidget(self)
        self.stack_widget.addTab(self.core_widget, 'Institution')
        self.model.add_command_contributer(self.core_widget)

        self.durations_widget = DurationsWidget(self)
        self.stack_widget.addTab(self.durations_widget, 'Time Periods')
        self.model.add_command_contributer(self.durations_widget)


    @QtCore.pyqtSlot()
    def load(self):
        self.model.clear_stack()
        filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Load Database File', '.db'))
        i = Institution()
        iso = InstitutionSavingObject(i,filename)
        iso.load()
        self.institution(i)

    @QtCore.pyqtSlot()
    def save(self):
        filename = str(QtGui.QFileDialog.getSaveFileName(self, 'Save Database File', '.db'))
        iso = InstitutionSavingObject(self._institution,filename)
        iso.createTables()
        iso.populateTables()


    @QtCore.pyqtSlot()
    def import_excell(self):
        self.model.clear_stack()
        filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Import population Excell File', '.xls'))
        if filename:
            saver = PopulationSavingObject([], filename)
            people = saver.load()
            self._institution.people += people
        filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Import duration Excell File', '.xls'))
        if filename:
            saver = DurationSavingObject(self.durations_widget.singleDurationWidget.duration, filename)
            saver.load(self._institution.people)
        self.institution(self._institution)

    @QtCore.pyqtSlot()
    def export_excell(self):
        filename = str(QtGui.QFileDialog.getSaveFileName(self, 'Export population Excell File', '.xls'))
        if filename:
            saver = PopulationSavingObject(self._institution.people, filename)
            saver.create()
            saver.populate()
        filename = str(QtGui.QFileDialog.getSaveFileName(self, 'Export duration Excell File', '.xls'))
        if filename:
            saver = DurationSavingObject(self.durations_widget.singleDurationWidget.duration, filename)
            saver.create()
            saver.populate()

    def institution(self, i):
        self._institution = i

        self.core_widget.institution(i)
        self.population_model = self.core_widget.population_model
        self.durations_widget.setPopulationModel(self.population_model)
        self.durations_widget.setInstitution(i)


import sys
from Rota_System.Institution import Institution


def main():
    app = QtGui.QApplication(sys.argv)
    w = InstitutionWidget(None)
    i = Institution()
    w.institution(i)
    w.show()

    v = QtGui.QUndoView(None)
    v.setStack(w.model.undoStack)
    v.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
