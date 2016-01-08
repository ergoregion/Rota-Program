__author__ = 'Neil Butcher'

import sqlite3
from Events import MultipleEventsSavingObject
from Rota_System.Duration import Duration


class DurationSavingObject(object):
    def __init__(self, durationList, filename):
        self._filename = filename
        self._durationList = durationList
        self._connection = sqlite3.connect(self._filename, detect_types=sqlite3.PARSE_DECLTYPES)

    def beginNew(self):
        with self._connection:
            self._removeTable()
            self._createTable()

    def _removeTable(self):
        _c = self._connection.cursor()
        try:
            _c.execute('''DROP TABLE Durations''')
        except sqlite3.OperationalError:
            pass

    def _emptyTable(self):
        _c = self._connection.cursor()
        _c.execute('''DELETE FROM Durations''')

    def _createTable(self):
        _c = self._connection.cursor()
        _c.execute('''CREATE TABLE Durations
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')

    def populateTables(self):
        for d in self._durationList:
            with self._connection:
                _c = self._connection.cursor()
                _c.execute('INSERT INTO Durations VALUES (?,?)', (None, d.name))
                lastRowID = _c.lastrowid
            e = MultipleEventsSavingObject(d.events, self._filename, lastRowID)
            e.populateTables()

    def loadTables(self, institution, personCacheDict=None):

        listOfDurationTupples = []

        with self._connection:
            _c = self._connection.cursor()
            for row in _c.execute('SELECT * FROM Durations'):
                d = Duration(institution)
                d.name = row[1]
                listOfDurationTupples.append((row[0], d))

        e = MultipleEventsSavingObject([], self._filename, 0)

        for t in listOfDurationTupples:
            e.loadEvents(t[1], t[0], personCacheDict)
            institution.durations.append(t[1])
