__author__ = 'Neil Butcher'

import unittest
from Rota_System.Institution import Institution
from Rota_System.Duration import Duration
from Rota_System.Events import Event, Appointment
from Rota_System.Saving.Excell import PopulationSavingObject, DurationSavingObject, ExcellImportExportError
from Rota_System.Roles import GlobalRoleList, Role, role
from Rota_System.Worker import Worker
from datetime import date
import os


def new_worker():
    bob = Worker()
    bob.name = 'Bob'
    bob.does_nothing()
    bob.add_role('S')
    bob.add_role('B')
    test_date = date(2012, 12, 31)
    test_date2 = date(2011, 12, 31)
    bob.clear_blacklist()
    bob.blacklist_date(test_date)
    bob.blacklist_date(test_date2)
    bob.phone_number = '0115'
    bob.address = 'a'
    bob.email = 'b'
    return bob


class Test(unittest.TestCase):
    def setUp(self):
        GlobalRoleList.add_role(Role('Baker', 'B', 10))
        GlobalRoleList.add_role(Role('Steward', 'S', 9))
        GlobalRoleList.add_role(Role('Fisherman', 'F', 7))
        GlobalRoleList.add_role(Role('Cook', 'C', 7))
        self.institution = Institution()
        self.duration = Duration(self.institution)

        e = Event(self.duration)
        e.title = 'A'
        e.add_appointment(Appointment(e, role("C"), e))
        e.add_appointment(Appointment(e, role("S"), e))
        e.appointments[1].note = 'with car'
        e.add_appointment(Appointment(e, role("F"), e))
        e.add_appointment(Appointment(e, role("F"), e))
        e.appointments[3].disabled = True
        e.add_appointment(Appointment(e, role("F"), e))
        self.duration.events.append(e)

        e = Event(self.duration)
        e.title = 'B'
        e.add_appointment(Appointment(e, role("F"), e))
        e.add_appointment(Appointment(e, role("F"), e))
        e.appointments[1].note = 'with car'
        e.add_appointment(Appointment(e, role("S"), e))
        e.appointments[2].note = 'with car'
        e.add_appointment(Appointment(e, role("B"), e))
        self.duration.events.append(e)

    def tearDown(self):
        GlobalRoleList.clear()

    def testSavePopulation(self):
        self.institution.people.append(new_worker())
        saver = PopulationSavingObject(self.institution.people, 'temp_sheet.xls')
        saver.create()
        saver.populate()

    def testSaveLoadPopulation(self):
        self.institution.people.append(new_worker())
        saver = PopulationSavingObject(self.institution.people, 'temp_sheet.xls')
        saver.create()
        saver.populate()

        loader = PopulationSavingObject([], 'temp_sheet.xls')
        loaded_population = loader.load()

        self.assertEqual(len(loaded_population), 1)

        loaded_person = loaded_population[0]
        self.assertEqual(loaded_person.name, 'Bob')
        self.assertEqual(loaded_person.address, 'a')
        self.assertEqual(loaded_person.email, 'b')
        self.assertEqual(loaded_person.phone_number, '0115')

        self.assertEqual(len(loaded_person.roles()), 2)
        self.assertTrue(loaded_person.suitable_for_role('B'))
        self.assertTrue(loaded_person.suitable_for_role('S'))
        self.assertFalse(loaded_person.suitable_for_role('F'))

    def testLoadPopulation(self):
        GlobalRoleList.clear()
        GlobalRoleList.add_role(Role('Doctor', 'D', 10))
        GlobalRoleList.add_role(Role('GP', 'G', 8))
        GlobalRoleList.add_role(Role('Nurse', 'N', 10))
        GlobalRoleList.add_role(Role('Cook', 'C', 7))
        GlobalRoleList.add_role(Role('Reception', 'R', 5))

        loader = PopulationSavingObject([], 'test_population_sheet.xls')
        loaded_population = loader.load()

        self.assertEqual(len(loaded_population), 6)

        loaded_person = loaded_population[0]
        self.assertEqual(loaded_person.name, 'Mary')
        self.assertEqual(loaded_person.address, 'A34')
        self.assertEqual(loaded_person.email, 'b')
        self.assertEqual(loaded_person.phone_number, '122')

        self.assertEqual(len(loaded_person.roles()), 2)
        self.assertTrue(loaded_person.suitable_for_role('D'))
        self.assertTrue(loaded_person.suitable_for_role('N'))
        self.assertFalse(loaded_person.suitable_for_role('C'))

        loaded_person = loaded_population[1]
        self.assertEqual(loaded_person.name, 'Jane')
        self.assertEqual(loaded_person.address, 'B32')
        self.assertEqual(loaded_person.email, 'g')
        self.assertEqual(loaded_person.phone_number, '463')

        self.assertEqual(len(loaded_person.roles()), 1)
        self.assertFalse(loaded_person.suitable_for_role('D'))
        self.assertTrue(loaded_person.suitable_for_role('G'))
        self.assertFalse(loaded_person.suitable_for_role('C'))

        loaded_person = loaded_population[2]
        self.assertEqual(loaded_person.name, 'Mick')

        self.assertEqual(len(loaded_person.roles()), 1)
        self.assertFalse(loaded_person.suitable_for_role('D'))
        self.assertTrue(loaded_person.suitable_for_role('C'))
        self.assertFalse(loaded_person.suitable_for_role('G'))

        loaded_person = loaded_population[3]
        self.assertEqual(loaded_person.name, 'John')

        self.assertEqual(len(loaded_person.roles()), 2)
        self.assertTrue(loaded_person.suitable_for_role('R'))
        self.assertTrue(loaded_person.suitable_for_role('N'))
        self.assertFalse(loaded_person.suitable_for_role('D'))

        loaded_person = loaded_population[4]
        self.assertEqual(loaded_person.name, 'Gaz')

        self.assertEqual(len(loaded_person.roles()), 1)
        self.assertFalse(loaded_person.suitable_for_role('D'))
        self.assertFalse(loaded_person.suitable_for_role('N'))
        self.assertTrue(loaded_person.suitable_for_role('C'))

        loaded_person = loaded_population[5]
        self.assertEqual(loaded_person.name, 'Toby')
        self.assertEqual(loaded_person.address, 'C16')
        self.assertEqual(loaded_person.email, '')
        self.assertEqual(loaded_person.phone_number, '400')

        self.assertEqual(len(loaded_person.roles()), 2)
        self.assertTrue(loaded_person.suitable_for_role('D'))
        self.assertTrue(loaded_person.suitable_for_role('G'))
        self.assertFalse(loaded_person.suitable_for_role('N'))

    def testInvalidLoadPopulation(self):
        GlobalRoleList.clear()
        GlobalRoleList.add_role(Role('Doctor', 'D', 10))
        GlobalRoleList.add_role(Role('GP', 'G', 8))
        GlobalRoleList.add_role(Role('Nurse', 'N', 10))
        GlobalRoleList.add_role(Role('Cook', 'C', 7))
        GlobalRoleList.add_role(Role('Reception', 'R', 5))

        loader = PopulationSavingObject([], 'test_invalid_population_sheet.xls')
        self.assertRaises(ExcellImportExportError, loader.load)

    def testDurationCreation(self):
        saver = DurationSavingObject(self.duration, 'temp_sheet.xls')
        saver.create()
        saver.populate()

    def testDurationPopulation(self):
        bob = new_worker()
        self.duration.events[1].appointments[2].appoint(bob)
        saver = DurationSavingObject(self.duration, 'temp_sheet.xls')
        saver.create()
        saver.populate()

    def testDurationEventsLoading(self):
        saver = DurationSavingObject(self.duration, 'temp_sheet.xls')
        saver.create()
        saver.populate()
        loader = DurationSavingObject(Duration(self.institution),'temp_sheet.xls')
        events = loader.load_events()
        self.assertEqual(len(events), len(self.duration.events))
        self.assertEqual(events[0].title, self.duration.events[0].title)
        self.assertEqual(events[1].time, self.duration.events[1].time)
        self.assertEqual(events[0].date, self.duration.events[0].date)

    def testDurationDisabledAppointmentLoading(self):
        saver = DurationSavingObject(self.duration, 'temp_sheet.xls')
        saver.create()
        saver.populate()
        for a in self.duration.appointments():
            a.disabled = False
        disabled_appointments = [a for a in self.duration.appointments() if a.disabled]
        self.assertTrue(len(disabled_appointments) == 0)
        loader = DurationSavingObject(self.duration, 'temp_sheet.xls')
        loader.load()
        disabled_appointments = [a for a in self.duration.appointments() if a.disabled]
        self.assertFalse(len(disabled_appointments) == 0)


    def testDurationFilledAppointmentLoading(self):
        bob = new_worker()
        key_appointment = self.duration.events[1].appointments[2]
        key_appointment.appoint(bob)
        self.assertTrue(key_appointment.is_filled())
        saver = DurationSavingObject(self.duration, 'temp_sheet.xls')
        saver.create()
        saver.populate()
        key_appointment.vacate()
        self.assertFalse(key_appointment.is_filled())
        loader = DurationSavingObject(self.duration, 'temp_sheet.xls')
        loader.load([bob])
        self.assertTrue(key_appointment.is_filled())

    def testAppointmentLoading(self):
        bob = new_worker()
        filled_appointments = [a for a in self.duration.appointments() if a.is_filled()]
        self.assertTrue(len(filled_appointments) == 0)
        loader = DurationSavingObject(self.duration, 'test_appointing_sheet.xls')
        loader.load([bob])
        filled_appointments = [a for a in self.duration.appointments() if a.is_filled()]
        self.assertEqual(len(filled_appointments),3)

    def testInvalidAppointmentLoading(self):
        bob = new_worker()
        loader = DurationSavingObject(self.duration, 'test_invalid_appointing_sheet.xls')
        self.assertRaises(ExcellImportExportError, loader.load, [bob])