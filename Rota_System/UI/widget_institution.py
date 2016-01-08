__author__ = 'Neil Butcher'

from PyQt4 import QtGui, QtCore
from widget_core import InstitutionCoreWidget
from widget_undobar import UndoBarWidget
from Duration import DurationsWidget

class InstitutionWidget(QtGui.QWidget):

    def __init__(self,parent = None):
        QtGui.QWidget.__init__(self,parent)

        self.layout = QtGui.QGridLayout(self)

        self.undoBar = UndoBarWidget(self)
        self.model = self.undoBar.model
        self.layout.addWidget(self.undoBar,0,1,1,2)

        self.stack_widget = QtGui.QTabWidget(self)
        self.layout.addWidget(self.stack_widget,1,0,1,8)


        self.core_widget = InstitutionCoreWidget(self)
        self.stack_widget.addTab(self.core_widget,'Institution')
        self.model.add_command_contributer(self.core_widget)

        self.durations_widget = DurationsWidget(self)
        self.stack_widget.addTab(self.durations_widget,'Time Periods')
        self.model.add_command_contributer(self.durations_widget)



    #
    # @QtCore.pyqtSlot()
    # def load(self):
    #     self.model.clearStack()
    #     filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Load Database File', '.db'))
    #     i = Institution()
    #     iso = InstitutionSavingObject(i,filename)
    #     iso.load()
    #     self.institution(i)
    #
    # @QtCore.pyqtSlot()
    # def save(self):
    #     filename = str(QtGui.QFileDialog.getSaveFileName(self, 'Save Database File', '.db'))
    #     iso = InstitutionSavingObject(self._institution,filename)
    #     iso.createTables()
    #     iso.populateTables()

    def institution(self,i):
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

    v=QtGui.QUndoView(None)
    v.setStack(w.model.undoStack)
    v.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
