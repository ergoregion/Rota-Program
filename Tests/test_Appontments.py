__author__ = 'Neil Butcher'

import unittest
from Rota_System import Appointments
from Rota_System import Roles


class AppointmentTest(unittest.TestCase):

    def setUp(self):
        Roles.GlobalRoleList.add_role(Roles.Role('Baker', 'B', 10))
        Roles.GlobalRoleList.add_role(Roles.Role('Steward', 'S', 9))
        Roles.GlobalRoleList.add_role(Roles.Role('Fisherman', 'F', 7))

    def tearDown(self):
        self.appointment = None
        Roles.GlobalRoleList.clear()

    def testNotes(self):

        r = Roles.role('B')

        self.appointment = Appointments.Appointment(None, r, None)
        self.assertEqual(self.appointment.note, '')
        self.appointment.note = 'a'
        self.assertEqual(self.appointment.note, 'a')
        self.appointment.note = ''
        self.assertEqual(self.appointment.note, '')
        self.appointment.note = 'treq'
        self.assertEqual(self.appointment.note, 'treq')
        self.appointment.note = '0909890'
        self.assertEqual(self.appointment.note, '0909890')

    def testDisabled(self):
        r = Roles.role('S')
        self.appointment = Appointments.Appointment(None, r, None)
        self.assertFalse(self.appointment.disabled)
        self.appointment.disabled = True
        self.assertTrue(self.appointment.disabled)

    def testRoles(self):

        r = Roles.role('B')
        self.appointment = Appointments.Appointment(None, r, None)
        self.assertEqual(self.appointment.role.code, 'B')
        self.assertNotEqual(self.appointment.role.code, 'F')
        self.assertEqual(self.appointment.role.description, 'Baker')
        self.assertEqual(self.appointment.role.priority, 10)

        r = Roles.role('F')
        self.appointment = Appointments.Appointment(None, r, None)
        self.assertEqual(self.appointment.role.code, 'F')
        self.assertNotEqual(self.appointment.role.code, 'B')
        self.assertEqual(self.appointment.role.description, 'Fisherman')
        self.assertEqual(self.appointment.role.priority, 7)

    def testUnfilled(self):

        r = Roles.role('B')
        self.appointment = Appointments.Appointment(None, r, None)
        self.assertFalse(self.appointment.is_filled())
        self.assertEqual(self.appointment._person, None)


class AppointmentPrototypeTest(unittest.TestCase):

    def setUp(self):
        Roles.GlobalRoleList.add_role(Roles.Role('Baker', 'B', 10))
        Roles.GlobalRoleList.add_role(Roles.Role('Steward', 'S', 9))
        Roles.GlobalRoleList.add_role(Roles.Role('Fisherman', 'F', 7))
        r = Roles.role('B')
        self.pt = Appointments.AppointmentPrototype(None, r)
        self.pt.note = 'hello'

    def tearDown(self):
        self.pt = None
        Roles.GlobalRoleList.clear()

    def testPrototype(self):
        self.assertEqual(self.pt.note, 'hello')
        self.assertEqual(self.pt.role.code, 'B')
        self.assertFalse(self.pt.disabled)

    def testAppointmentCreation(self):
        app = self.pt.create_in(None)
        self.assertEqual(self.pt.note, app.note)
        self.assertEqual(self.pt.role.code, app.role.code)
        self.assertEqual(self.pt.disabled, app.disabled)
        self.assertEqual(app.event, None)

    def testChangesAndAppointmentCreation(self):
        self.pt.note = 'a'
        app = self.pt.create_in(None)
        self.assertEqual(self.pt.note, app.note)
        self.assertEqual(self.pt.role.code, app.role.code)
        self.assertEqual(self.pt.disabled, app.disabled)

        self.pt.disabled = True
        app = self.pt.create_in(None)
        self.assertEqual(self.pt.note, app.note)
        self.assertEqual(self.pt.role.code, app.role.code)
        self.assertEqual(self.pt.disabled, app.disabled)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()