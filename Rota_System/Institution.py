__author__ = 'Neil Buther'


from PyQt4.QtCore import pyqtSignal, QObject


class Institution(QObject):
    """
    storage of all people
    """
    populationChanged = pyqtSignal()

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.name = 'Institution'
        self.people = []