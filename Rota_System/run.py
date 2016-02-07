__author__= 'Neil Butcher'

import sys
from Rota_System.UI import InstitutionWidget
from PyQt4 import QtGui
from Rota_System.Institution import Institution

def main():
    app = QtGui.QApplication(sys.argv)
    w = InstitutionWidget(None)
    i = Institution()
    w.institution(i)
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
