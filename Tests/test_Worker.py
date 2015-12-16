__author__ = 'Neil Butcher'

'''
Created on 8 Oct 2012

@author: neil
'''
import unittest
from Rota_System.Worker import Worker
from Rota_System import Roles


class WorkerTest(unittest.TestCase):
    def setUp(self):
        self.bob = Worker()
        self.bob.name = 'Bob'
        Roles.GlobalRoleList.add_role(Roles.Role('Plumber', 'P', 1))
        Roles.GlobalRoleList.add_role(Roles.Role('Sailor', 'S', 1))
        Roles.GlobalRoleList.add_role(Roles.Role('Treasurer', 'T', 9))

    def tearDown(self):
        self.bob = None
        Roles.GlobalRoleList.clear()

    def testName(self):
        self.assertEqual(self.bob.name, 'Bob')

    def testNoRole(self):
        self.bob.does_nothing()
        self.assertEqual(self.bob.number_of_roles(), 0)

    def testAddRole(self):
        self.bob.does_nothing()
        self.bob.add_role('S')
        self.assertEqual(self.bob.number_of_roles(), 1)
        self.bob.add_role('P')
        self.assertEqual(self.bob.number_of_roles(), 2)
        self.bob.add_role('S')
        self.assertEqual(self.bob.number_of_roles(), 2)

    def testRemoveRole(self):
        self.bob.does_nothing()
        self.bob.add_roles('S P T P')
        self.assertEqual(self.bob.number_of_roles(), 3)
        self.bob.remove_role('P')
        self.assertEqual(self.bob.number_of_roles(), 2)
        self.bob.remove_role('S')
        self.assertEqual(self.bob.number_of_roles(), 1)

    def testSuitableForRole(self):
        self.bob.does_nothing()
        self.bob.add_roles('S P T P')
        self.assertTrue(self.bob.suitable_for_role('P'))
        self.assertTrue(self.bob.suitable_for_role('S'))
        self.assertTrue(self.bob.suitable_for_role('T'))
        self.bob.remove_role('P')
        self.assertFalse(self.bob.suitable_for_role('P'))
        self.assertTrue(self.bob.suitable_for_role('S'))
        self.assertTrue(self.bob.suitable_for_role('T'))
        self.bob.remove_role('S')
        self.assertFalse(self.bob.suitable_for_role('P'))
        self.assertFalse(self.bob.suitable_for_role('S'))
        self.assertTrue(self.bob.suitable_for_role('T'))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
