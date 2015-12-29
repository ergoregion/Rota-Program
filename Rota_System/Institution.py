__author__ = 'Neil Butcher'


from PyQt4.QtCore import pyqtSignal, QObject


class Institution(QObject):
    """
    storage of all people
    storage of a list of templates used to create events
    storage of a list of durations used to sort events
    """
    populationChanged = pyqtSignal()

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.name = 'Institution'
        self.people = []
        self.templates = []
        self.durations = []