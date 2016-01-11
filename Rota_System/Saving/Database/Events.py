__author__ = 'Neil Butcher'

import sqlite3
from Rota_System.Appointments import Appointment
from Rota_System.Events import Event, EventPrototype
from datetime import datetime, date
from Rota_System.Roles import role


class MultipleEventsSavingObject(object):
    '''
    classdocs
    '''

    def __init__(self, eventsList, filename, duration=None):
        self._filename = filename
        self._eventsList = eventsList
        self._duration = duration
        self._connection = sqlite3.connect(self._filename, detect_types=sqlite3.PARSE_DECLTYPES)

    def beginNew(self):
        with self._connection:
            self._removeTable()
            self._createTable()

    def _removeTable(self):
        _c = self._connection.cursor()
        try:
            _c.execute('''DROP TABLE Appointments''')
            _c.execute('''DROP TABLE Events''')
        except sqlite3.OperationalError:
            pass

    def _createTable(self):
        _c = self._connection.cursor()
        _c.execute('''CREATE TABLE Appointments
             (id INTEGER PRIMARY KEY AUTOINCREMENT, note TEXT, disabled INTEGER, role TEXT,person TEXT,event INTEGER)''')
        _c.execute('''CREATE TABLE Events
             (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, notes TEXT, description TEXT,name TEXT,datetime TIMESTAMP, templateType INTEGER, duration Integer)''')

    def _emptyTable(self):
        _c = self._connection.cursor()
        _c.execute('''DELETE FROM Events''')
        _c.execute('''DELETE FROM Appointments''')

    def tableTupple(self, event, durationIndex):
        if event.template:
            return None, event.title, event.notes, event.description, event.name, datetime.combine(date(0001, 01, 01),
                                                                                                   event.time), 1, 0
        else:
            return None, event.title, event.notes, event.description, None, event.datetime(), 0, durationIndex

    @staticmethod
    def appointmentTableTupple(appointment, eventIndex):
        if appointment.disabled:
            disabledIndex = 1
        else:
            disabledIndex = 0

        if appointment.person:
            personText = appointment.person.name
        else:
            personText = ''

        return None, appointment.note, disabledIndex, appointment.role.description, personText, eventIndex

    def populateTables(self):
        with self._connection:
            _c = self._connection.cursor()

            for e in self._eventsList:
                tupple = self.tableTupple(e, self._duration)
                _c.execute('INSERT INTO Events VALUES (?,?,?,?,?,?,?,?)', tupple)
                lastRowID = _c.lastrowid
                for a in e.appointments:
                    tupple = self.appointmentTableTupple(a, lastRowID)
                    _c.execute('INSERT INTO Appointments VALUES (?,?,?,?,?,?)', tupple)

    def loadEvents(self, parent, durationIndex=None, personCacheDict=None):

        if durationIndex:
            dx = durationIndex
            tx = 0
        else:
            dx = 0
            tx = 1

        listOfEvents = []

        with self._connection:
            _c = self._connection.cursor()
            _c.execute('SELECT * FROM Events WHERE templateType = ? AND duration = ?', (tx, dx))
            for row in _c.fetchall():
                dt = row[5]
                if durationIndex:
                    e = Event(parent)
                    e._datetime = dt
                else:
                    e = EventPrototype(parent)
                    e.time = dt.time()
                    e.name = row[4]
                e.title = row[1]
                e.notes = row[2]
                e.description = row[3]
                appointmentsOfThisEvent = []
                for row in _c.execute('SELECT * FROM Appointments WHERE event = ?', (row[0],)):
                    r = role(row[3])
                    a = Appointment(e, r, e)
                    a.note = row[1]
                    if row[2] == 1:
                        a.disabled = True
                    if personCacheDict and len(row[4]) > 0:
                        p = personCacheDict[row[4]]
                        a.appoint(p)
                    appointmentsOfThisEvent.append(a)
                e.appointments = appointmentsOfThisEvent
                listOfEvents.append(e)

        if durationIndex:
            parent.events = listOfEvents
        else:
            parent.templates = listOfEvents
