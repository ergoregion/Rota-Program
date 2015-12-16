__author__ = 'Neil Butcher'

from PyQt4.QtCore import pyqtSignal, QObject


class Person(QObject):

    dataChanged = pyqtSignal(QObject)
    nameChanged = pyqtSignal(QObject)

    def __init__(self, parent=None):
        super(Person, self).__init__(parent)
        self._blacklisted_dates = []
        self._name = 'A New Person'
        self._phone_number = ''
        self._email = ''
        self._address = ''

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.dataChanged.emit(self)
        self.nameChanged.emit(self)

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        self._phone_number = value
        if not value:
            self._phone_number = ''
        self.dataChanged.emit(self)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value
        if not value:
            self._email = ''
        self.dataChanged.emit(self)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value
        if not value:
            self._address = ''
        self.dataChanged.emit(self)

    def __str__(self):
        return str(self.name)

    def clear_blacklist(self):
        self._blacklisted_dates = []
        self.dataChanged.emit(self)

    def blacklist_date(self, a_date):
        if a_date in self._blacklisted_dates:
            return self
        self._blacklisted_dates.append(a_date)
        self.dataChanged.emit(self)

    def free_date(self, a_date):
        if a_date in self._blacklisted_dates:
            self._blacklisted_dates.remove(a_date)
            self.dataChanged.emit(self)

    def blacklisted_dates(self):
        return self._blacklisted_dates

    def is_available_on_date(self, a_date):
        return a_date not in self._blacklisted_dates