__author__ = 'Neil Butcher'

import unittest
from Rota_System.Institution import Institution
from Rota_System.Saving.Database import InstitutionSavingObject
from Rota_System.Roles import GlobalRoleList, Role
from Rota_System.Worker import Worker
from datetime import date
from Rota_System.StandardTimes import StandardEventTimes

def newWorker():
    bob = Worker()
    bob.name = ('Bob')
    bob.does_nothing()
    bob.add_role('S')
    bob.add_role('B')
    testDate = date(2012,12,31)
    testDate2 = date(2011,12,31)
    bob.clear_blacklist()
    bob.blacklist_date(testDate)
    bob.blacklist_date(testDate2)
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
        self.saver = InstitutionSavingObject(self.institution,'database.db')


    def tearDown(self):
        GlobalRoleList.clear()


    def testSaveLoadTimes(self):
        self.assertGreater(len(StandardEventTimes), 0, 'The times have not been defined')
        self.saver.createTables()
        self.saver.populateTables()

        StandardEventTimes[:] = []
        self.assertEqual(len(StandardEventTimes),0)

        self.saver.loadTimes()
        self.assertGreater(len(StandardEventTimes), 0, 'The times have not been imported')

        pass

    def testloadRoles(self):

        self.assertGreater(len(GlobalRoleList.roles), 0, 'The roles have not been defined')

        self.saver.createTables()
        self.saver.populateTables()

        GlobalRoleList.clear()
        self.assertEqual(len(GlobalRoleList.roles),0)

        self.saver.loadRoles()

        self.assertGreater(len(GlobalRoleList.roles), 0, 'The roles have not been repopulated')

        role1 = GlobalRoleList.role_from_desc('Baker')
        role2 = GlobalRoleList.role_from_desc('Fisherman')
        self.assertFalse(role1.compatible_with(role2))

    def testloadRolesCompatibilities(self):

        self.assertGreater(len(GlobalRoleList.roles), 0, 'The roles have not been defined')

        role1 = GlobalRoleList.role_from_desc('Steward')
        role2 = GlobalRoleList.role_from_desc('Cook')
        role1.compatibilities.add(role2)
        role2.compatibilities.add(role1)

        role1 = GlobalRoleList.role_from_desc('Baker')
        role2 = GlobalRoleList.role_from_desc('Fisherman')
        role1.compatibilities.add(role2)
        role2.compatibilities.add(role1)

        self.saver.createTables()
        self.saver.populateTables()
        GlobalRoleList.clear()
        self.saver.loadRoles()

        role1 = GlobalRoleList.role_from_desc('Baker')
        role2 = GlobalRoleList.role_from_desc('Fisherman')
        self.assertTrue(role1.compatible_with(role2))

        role1 = GlobalRoleList.role_from_desc('Fisherman')
        role2 = GlobalRoleList.role_from_desc('Steward')
        self.assertFalse(role1.compatible_with(role2))

        role1 = GlobalRoleList.role_from_desc('Baker')
        role2 = GlobalRoleList.role_from_desc('Cook')
        self.assertFalse(role1.compatible_with(role2))

        role1 = GlobalRoleList.role_from_desc('Steward')
        role2 = GlobalRoleList.role_from_desc('Cook')
        self.assertTrue(role1.compatible_with(role2))


    def testloadPopulation(self):
        self.institution.people.append(newWorker())
        self.saver.createTables()
        self.saver.populateTables()

        self.institution.people = []
        self.assertEqual(len(self.institution.people),0)

        self.saver.loadPopulation()
        self.assertEqual(len(self.institution.people),1)

        loadedPerson = self.institution.people[0]
        self.assertEqual(loadedPerson.name,'Bob')
        self.assertEqual(loadedPerson.address,'a')
        self.assertEqual(loadedPerson.email,'b')
        self.assertEqual(loadedPerson.phoneNumber,'0115')

        self.assertEqual(len(loadedPerson._blacklisted_dates) , 2)
        self.assertFalse(loadedPerson.is_available_on_date(date(2012,12,31)))
        self.assertFalse(loadedPerson.is_available_on_date(date(2011,12,31)))
        self.assertTrue(loadedPerson.is_available_on_date(date(2011,12,30)))

        self.assertEqual(len(loadedPerson.roles()),2)
        self.assertTrue(loadedPerson.suitable_for_role('B'))
        self.assertTrue(loadedPerson.suitable_for_role('S'))
        self.assertFalse(loadedPerson.suitable_for_role('F'))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()