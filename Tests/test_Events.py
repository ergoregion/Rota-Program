__author__ = 'Neil Butcher'

import unittest
from Rota_System import Appointments
from Rota_System import Events
from Rota_System import Roles
from datetime import time


class EventTest(unittest.TestCase):
    def setUp(self):
        Roles.GlobalRoleList.add_role(Roles.Role('Baker', 'B', 10))
        Roles.GlobalRoleList.add_role(Roles.Role('Steward', 'S', 9))
        Roles.GlobalRoleList.add_role(Roles.Role('Fisherman', 'F', 7))
        self.event = Events.Event(None)

    def tearDown(self):
        self.event = None
        Roles.GlobalRoleList.clear()

    def testProperties(self):
        self.assertEqual(self.event.title, '')
        self.event.title = 'Making Breakfast'
        self.assertEqual(self.event.title, 'Making Breakfast')

        self.assertEqual(self.event.description, '')
        self.event.description = 'A meal of bread and fish'
        self.assertEqual(self.event.title, 'Making Breakfast')
        self.assertEqual(self.event.description, 'A meal of bread and fish')

        self.assertEqual(self.event.notes, '')
        self.event.notes = 'also requires someone to serve'
        self.assertEqual(self.event.title, 'Making Breakfast')
        self.assertEqual(self.event.description, 'A meal of bread and fish')
        self.assertEqual(self.event.notes, 'also requires someone to serve')


class EventPrototypeTest(unittest.TestCase):

    def setUp(self):
        self.pt = Events.EventPrototype(None)
        self.pt.title = 'Making Breakfast'
        self.pt.description = 'A meal of bread and fish'
        self.pt.notes = 'also requires someone to serve'

    def tearDown(self):
        self.pt = None

    def testProperties(self):
        self.assertEqual(self.pt.title, 'Making Breakfast')
        self.assertEqual(self.pt.description, 'A meal of bread and fish')
        self.assertEqual(self.pt.notes, 'also requires someone to serve')

    def testName(self):
        self.assertEqual(self.pt.name, 'New Template')
        self.pt.name = 'A standard breakfast'
        self.assertEqual(self.pt.name, 'A standard breakfast')

    def testTime(self):
        self.assertEqual(self.pt.time, time(9, 0, 0))
        self.pt.time = time(11, 0, 0)
        self.assertEqual(self.pt.time, time(11, 0, 0))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()