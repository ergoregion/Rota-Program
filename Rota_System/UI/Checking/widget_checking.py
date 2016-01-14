__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from Rota_System.Evaluation import CheckDuration


class CheckingWidget(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QHBoxLayout(self)

        self._button = QtGui.QPushButton('Error Check', self)
        self._button.clicked.connect(self._check_button_pushed)
        self.layout.addWidget(self._button)
        self._errors_list_widget = QtGui.QListWidget(self)
        self.layout.addWidget(self._errors_list_widget)

    def population(self, population):
        self._population = population

    def duration(self, duration):
        self._duration = duration
        self._refresh()

    @QtCore.pyqtSlot()
    def _check_button_pushed(self):
        self._refresh()

    def _refresh(self):
        self._errors_list_widget.clear()
        if self._duration is not None and self._population is not None:
            list_of_errors = CheckDuration(self._duration, self._population)
            for e in list_of_errors:
                i = QtGui.QListWidgetItem(e.text, self._errors_list_widget)
                i.setTextColor(QtGui.QColor(e.color))
                self._errors_list_widget.addItem(i)



import sys
from Rota_System.Roles import Role, GlobalRoleList
from Rota_System import Duration
from Rota_System.UI.model_undo import MasterUndoModel


def main():
    GlobalRoleList.add_role(Role('Baker', 'B', 2))
    GlobalRoleList.add_role(Role('Singer', 'S', 9))
    GlobalRoleList.add_role(Role('Fisherman', 'F', 7))

    app = QtGui.QApplication(sys.argv)
    w = CheckingWidget(None)
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()