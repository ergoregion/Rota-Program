__author__ = 'Neil Butcher'

import unittest
from Rota_System import Roles


class RoleTest(unittest.TestCase):
    def setUp(self):
        Roles.GlobalRoleList.clear()
        Roles.GlobalRoleList.add_role(Roles.Role('Preacher', 'P', 10))
        Roles.GlobalRoleList.add_role(Roles.Role('Steward', 'S', 9))
        Roles.GlobalRoleList.add_role(Roles.Role('Finance Steward', 'F', 7))

    def tearDown(self):
        Roles.GlobalRoleList.clear()

    def testOuterCreation(self):
        preacher = Roles.role_from_code('P')
        self.assertEqual(preacher.code, 'P')
        self.assertEqual(preacher.description, 'Preacher')
        preacher = Roles.role('P')
        self.assertEqual(preacher.code, 'P')
        self.assertEqual(preacher.description, 'Preacher')
        preacher = Roles.role('Preacher')
        self.assertEqual(preacher.code, 'P')
        self.assertEqual(preacher.description, 'Preacher')

    def testCreation(self):
        preacher = Roles.role('P')
        self.assertEqual(preacher.code, 'P')
        self.assertEqual(preacher.description, 'Preacher')

    def testListCreation(self):
        roles = Roles.RoleList()
        roles.all()
        preacher = roles.role_from_code('P')
        self.assertEqual(preacher.code, 'P')
        self.assertEqual(preacher.description, 'Preacher')
        preacher = roles.role_from_code('P  ')
        self.assertEqual(preacher.code, 'P')
        self.assertEqual(preacher.description, 'Preacher')

    def testListInitCreation(self):
        roles = Roles.RoleList('P')
        self.assertEqual(len(roles.roles), 1, 'should be a role already')

    def testLookup(self):
        roles = Roles.RoleList()
        roles.all()
        self.assertTrue(roles.includes('S'), 'All roles should include steward')
        self.assertTrue(roles.includes('P'), 'All roles should include preacher')
        self.assertTrue(roles.includes(Roles.role('P')), 'All roles should include preacher as class')
        self.assertTrue(roles.includes('S     '), 'All roles should include steward')

    def testSinglePopulatedList(self):
        roles = Roles.RoleList()
        roles.populate_from_codes('S')
        self.assertFalse(roles.includes('P'), 'this list should not include preacher')
        self.assertTrue(roles.includes(Roles.role('S')), 'This list should include steward')
        self.assertTrue(roles.includes('S     '), 'This list should include steward')

    def testSingleAddedList(self):
        roles = Roles.RoleList()
        roles.add_code('S')
        self.assertFalse(roles.includes('P'), 'this list should not include preacher')
        self.assertTrue(roles.includes(Roles.role('S')), 'This list should include steward')
        self.assertTrue(roles.includes('S     '), 'This list should include steward')
        self.assertEqual(roles.number_of_roles(), 1)
        roles.add_code('S')
        self.assertEqual(roles.number_of_roles(), 1)
        roles.add_code('P')
        self.assertEqual(roles.number_of_roles(), 2)

    def testMultiPopulatedList(self):
        roles = Roles.RoleList()
        roles.populate_from_codes('F S')
        self.assertFalse(roles.includes('P'), 'this list should not include preacher')
        self.assertTrue(roles.includes(Roles.role('Steward')), 'This list should include steward')
        self.assertTrue(roles.includes(Roles.role('F')), 'This list should also include finance steward')

    def testMultiAddedList(self):
        roles = Roles.RoleList()
        roles.add_code('S')
        self.assertEqual(roles.number_of_roles(), 1)
        roles.add_code('F')
        roles.add_code('S')
        self.assertEqual(roles.number_of_roles(), 2)
        self.assertFalse(roles.includes('P'), 'this list should not include preacher')
        self.assertTrue(roles.includes(Roles.role('S')), 'This list should include steward')
        self.assertTrue(roles.includes(Roles.role('Finance Steward')), 'This list should also include finance steward')

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
        roles.remove_code('P')
        self.assertEqual(roles.number_of_roles(), 1)
        roles.add_code('S')
        roles.add_code('P')
        self.assertEqual(roles.number_of_roles(), 3)

    def testOutputList(self):
        roles = Roles.RoleList()
        roles.populate_from_codes('F S')
        self.assertTrue('F' in roles.list_of_codes().split())
        self.assertTrue('S' in roles.list_of_codes().split())
        self.assertFalse('P' in roles.list_of_codes().split())
        roles.all()
        self.assertTrue('F' in roles.list_of_codes().split())
        self.assertTrue('S' in roles.list_of_codes().split())
        self.assertTrue('P' in roles.list_of_codes().split())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()