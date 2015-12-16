__author__ = 'Neil Butcher'

import unittest
from Rota_System import Roles


class RoleTest(unittest.TestCase):
    def setUp(self):
        Roles.GlobalRoleList.clear()
        Roles.GlobalRoleList.add_role(Roles.Role('Baker', 'B', 10))
        Roles.GlobalRoleList.add_role(Roles.Role('Steward', 'S', 9))
        Roles.GlobalRoleList.add_role(Roles.Role('Fisherman', 'F', 7))

    def tearDown(self):
        Roles.GlobalRoleList.clear()

    def testOuterCreation(self):
        baker = Roles.role_from_code('B')
        self.assertEqual(baker.code, 'B')
        self.assertEqual(baker.description, 'Baker')
        baker = Roles.role('B')
        self.assertEqual(baker.code, 'B')
        self.assertEqual(baker.description, 'Baker')
        baker = Roles.role('Baker')
        self.assertEqual(baker.code, 'B')
        self.assertEqual(baker.description, 'Baker')

    def testCreation(self):
        baker = Roles.role('B')
        self.assertEqual(baker.code, 'B')
        self.assertEqual(baker.description, 'Baker')

    def testListCreation(self):
        roles = Roles.RoleList()
        roles.all()
        baker = roles.role_from_code('B')
        self.assertEqual(baker.code, 'B')
        self.assertEqual(baker.description, 'Baker')
        baker = roles.role_from_code('B  ')
        self.assertEqual(baker.code, 'B')
        self.assertEqual(baker.description, 'Baker')

    def testListInitCreation(self):
        roles = Roles.RoleList('B')
        self.assertEqual(len(roles.roles), 1, 'should be a role already')

    def testLookup(self):
        roles = Roles.RoleList()
        roles.all()
        self.assertTrue(roles.includes('S'), 'All roles should include steward')
        self.assertTrue(roles.includes('B'), 'All roles should include baker')
        self.assertTrue(roles.includes(Roles.role('B')), 'All roles should include baker as class')
        self.assertTrue(roles.includes('S     '), 'All roles should include steward')

    def testSinglePopulatedList(self):
        roles = Roles.RoleList()
        roles.populate_from_codes('S')
        self.assertFalse(roles.includes('B'), 'this list should not include baker')
        self.assertTrue(roles.includes(Roles.role('S')), 'This list should include steward')
        self.assertTrue(roles.includes('S     '), 'This list should include steward')

    def testSingleAddedList(self):
        roles = Roles.RoleList()
        roles.add_code('S')
        self.assertFalse(roles.includes('B'), 'this list should not include baker')
        self.assertTrue(roles.includes(Roles.role('S')), 'This list should include steward')
        self.assertTrue(roles.includes('S     '), 'This list should include steward')
        self.assertEqual(roles.number_of_roles(), 1)
        roles.add_code('S')
        self.assertEqual(roles.number_of_roles(), 1)
        roles.add_code('B')
        self.assertEqual(roles.number_of_roles(), 2)

    def testMultiPopulatedList(self):
        roles = Roles.RoleList()
        roles.populate_from_codes('F S')
        self.assertFalse(roles.includes('B'), 'this list should not include baker')
        self.assertTrue(roles.includes(Roles.role('Steward')), 'This list should include steward')
        self.assertTrue(roles.includes(Roles.role('F')), 'This list should also include fisherman')

    def testMultiAddedList(self):
        roles = Roles.RoleList()
        roles.add_code('S')
        self.assertEqual(roles.number_of_roles(), 1)
        roles.add_code('F')
        roles.add_code('S')
        self.assertEqual(roles.number_of_roles(), 2)
        self.assertFalse(roles.includes('B'), 'this list should not include baker')
        self.assertTrue(roles.includes(Roles.role('S')), 'This list should include steward')
        self.assertTrue(roles.includes(Roles.role('Fisherman')), 'This list should also include fisherman')

    def testRemovingList(self):
        roles = Roles.RoleList()
        roles.add_code('S')
        self.assertEqual(roles.number_of_roles(), 1)
        roles.remove_code('S')
        roles.remove_code('F')
        self.assertEqual(roles.number_of_roles(), 0)
        roles.add_code(' S')
        roles.add_code('F ')
        self.assertEqual(roles.number_of_roles(), 2)
        roles.remove_code('S')
        roles.remove_code('B')
        self.assertEqual(roles.number_of_roles(), 1)
        roles.add_code('S')
        roles.add_code('B')
        self.assertEqual(roles.number_of_roles(), 3)

    def testOutputList(self):
        roles = Roles.RoleList()
        roles.populate_from_codes('F S')
        self.assertTrue('F' in roles.list_of_codes().split())
        self.assertTrue('S' in roles.list_of_codes().split())
        self.assertFalse('B' in roles.list_of_codes().split())
        roles.all()
        self.assertTrue('F' in roles.list_of_codes().split())
        self.assertTrue('S' in roles.list_of_codes().split())
        self.assertTrue('B' in roles.list_of_codes().split())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()