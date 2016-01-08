__author__ = 'Neil Butcher'

import sqlite3
from Events import MultipleEventsSavingObject
from Rota_System.Roles import GlobalRoleList, Role
from Rota_System.StandardTimes import StandardEventTimes
from Rota_System.Worker import Worker
from Duration import DurationSavingObject
from Error import DatabaseSaveLoadError
import time
from datetime import datetime


class InstitutionSavingObject(object):
    '''
    classdocs
    '''

    def __init__(self, institution, filename=None):
        if filename:
            self._filename = filename
        else:
            self._filename = institution.name + '.db'

        self._institution = institution
        self._connection = sqlite3.connect(self._filename, detect_types=sqlite3.PARSE_DECLTYPES)

    def load(self):

        self.loadRoles()
        self.loadTimes()
        self.loadPopulation()
        self.loadTemplates()
        self.loadDurations()

    def createTables(self):
        with self._connection:
            self._createRolesTables()
            self._createPopulationTables()
            self._createTimesTable()
        MultipleEventsSavingObject(None, self._filename, None).beginNew()
        DurationSavingObject(None, self._filename).beginNew()

    def populateTables(self):
        with self._connection:
            self._populateRolesTables()
            self._populatePopulationTables()
            self._populateTimesTable()
        e = MultipleEventsSavingObject(self._institution.templates, self._filename, None)
        d = DurationSavingObject(self._institution.durations, self._filename)
        e.populateTables()
        d.populateTables()

    def loadTemplates(self):
        MultipleEventsSavingObject(None, self._filename, None).loadEvents(self._institution)

    def loadDurations(self):
        if self._personCacheDict:
            DurationSavingObject(None, self._filename).loadTables(self._institution, self._personCacheDict)
        else:
            raise DatabaseSaveLoadError('The population must be loaded before appointments can be loaded')

    def loadTimes(self):
        with self._connection:
            self._loadInTimesTable()

    def loadRoles(self):
        with self._connection:
            self._loadInRolesTables()

    def loadPopulation(self):
        with self._connection:
            self._loadInRolesTables()
            self._loadInPopulationTables()

    def _createRolesTables(self):
        _c = self._connection.cursor()
        try:
            _c.execute('''DROP TABLE Roles''')
        except sqlite3.OperationalError:
            pass
        _c.execute('''CREATE TABLE Roles
             (description TEXT NOT NULL, priority INTEGER, code TEXT,PRIMARY KEY (description))''')
        try:
            _c.execute('''DROP TABLE RolesCompatibility''')
        except sqlite3.OperationalError:
            pass
        _c.execute('''CREATE TABLE RolesCompatibility
             (role1Description TEXT NOT NULL, role2Description TEXT NOT NULL)''')

    @staticmethod
    def roleTupple(role):
        return role.description, role.priority, role.code

    def _populateRolesTables(self):
        _c = self._connection.cursor()
        _c.execute('''DELETE FROM Roles''')
        roleTupples = map(self.roleTupple, GlobalRoleList.roles)
        _c.executemany('INSERT INTO Roles VALUES (?,?,?)', roleTupples)

        _c.execute('''DELETE FROM RolesCompatibility''')
        for role1 in GlobalRoleList.roles:
            for role2 in role1.compatibilities.roles:
                _c.execute('INSERT INTO RolesCompatibility VALUES (?,?)', (role1.description, role2.description))

    def _loadInRolesTables(self):
        _c = self._connection.cursor()
        GlobalRoleList.clear()
        for row in _c.execute('SELECT * FROM Roles ORDER BY priority'):
            GlobalRoleList.add_role(Role(row[0], row[2], row[1]))

        for row in _c.execute('SELECT * FROM RolesCompatibility'):
            role1 = GlobalRoleList.role_from_desc(row[0])
            role2 = GlobalRoleList.role_from_desc(row[1])
            role1.compatibilities.add(role2)

    def _createPopulationTables(self):
        _c = self._connection.cursor()
        try:
            _c.execute('''DROP TABLE Population''')
        except sqlite3.OperationalError:
            pass
        _c.execute('''CREATE TABLE Population
             (name TEXT NOT NULL, address TEXT, email TEXT, phone TEXT,PRIMARY KEY (name))''')
        try:
            _c.execute('''DROP TABLE PopulationAvailability''')
        except sqlite3.OperationalError:
            pass
        _c.execute('''CREATE TABLE PopulationAvailability
             (personName TEXT NOT NULL, unavailableDate date NOT NULL)''')
        self._connection.commit()
        try:
            _c.execute('''DROP TABLE PopulationQualifications''')
        except sqlite3.OperationalError:
            pass
        _c.execute('''CREATE TABLE PopulationQualifications
             (personName TEXT NOT NULL, qualification TEXT NOT NULL)''')

    @staticmethod
    def personTupple(person):
        return person.name, person.address, person.email, person.phone_number

    def _populatePopulationTables(self):
        _c = self._connection.cursor()
        _c.execute('''DELETE FROM Population''')
        tupples = map(self.personTupple, self._institution.people)
        _c.executemany('INSERT INTO Population VALUES (?,?,?,?)', tupples)

        _c.execute('''DELETE FROM PopulationAvailability''')
        _c.execute('''DELETE FROM PopulationQualifications''')
        for person in self._institution.people:
            for date in person.blacklisted_dates():
                _c.execute('INSERT INTO PopulationAvailability VALUES (?,?)', (person.name, date))
            for role in person.roles():
                _c.execute('INSERT INTO PopulationQualifications VALUES (?,?)', (person.name, role.description))

    def _loadInPopulationTables(self):
        _c = self._connection.cursor()
        self._institution.people = []
        personCacheDict = {'Name': 'PersonObject'}
        for row in _c.execute('SELECT * FROM Population ORDER BY name'):
            p = Worker()
            p.name = row[0]
            p.address = row[1]
            p.email = row[2]
            p.phoneNumber = row[3]
            self._institution.people.append(p)
            personCacheDict[p.name] = p

        for row in _c.execute('SELECT * FROM PopulationAvailability'):
            personCacheDict[row[0]].blacklist_date(row[1])

        for row in _c.execute('SELECT * FROM PopulationQualifications'):
            r = GlobalRoleList.role_from_desc(row[1])
            personCacheDict[row[0]].roles().add(r)

        self._personCacheDict = personCacheDict

    def _createTimesTable(self):
        _c = self._connection.cursor()
        try:
            _c.execute('''DROP TABLE StandardEventTimes''')
        except sqlite3.OperationalError:
            pass
        _c.execute('''CREATE TABLE StandardEventTimes
             (name TEXT NOT NULL, time TEXT,PRIMARY KEY (name))''')

    @staticmethod
    def timeTupple(item):
        return item[0], item[1].strftime("%H:%M")

    def _populateTimesTable(self):
        _c = self._connection.cursor()
        _c.execute('''DELETE FROM StandardEventTimes''')
        timeTupples = map(self.timeTupple, StandardEventTimes)
        _c.executemany('INSERT INTO StandardEventTimes VALUES (?,?)', timeTupples)

    def _loadInTimesTable(self):
        _c = self._connection.cursor()
        StandardEventTimes[:] = []
        for row in _c.execute('SELECT * FROM StandardEventTimes'):
            t = (datetime(*time.strptime(row[1], "%H:%M")[0:6])).time()
            StandardEventTimes.append((row[0], t))
