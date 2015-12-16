__author__ = 'Neil Butcher'

import unittest
from Rota_System.Person import Person
from datetime import date


class PersonTest(unittest.TestCase):
    bob = None

    def setUp(self):
        self.bob = Person()
        self.bob.name = 'Bob'

    def tearDown(self):
        self.bob = None

    def testName(self):
        self.assertEqual(self.bob.name, 'Bob')

    def testPhoneNumber(self):
        self.bob.phone_number = '999'
        self.assertEqual(self.bob.phone_number, '999')
        self.bob.phone_number = '112'
        self.assertNotEqual(self.bob.phone_number, '999')
        self.assertEqual(self.bob.phone_number, '112')

    def testNamePhone(self):
        self.bob.phone_number = '999'
        self.assertEqual(self.bob.name, 'Bob')
        self.assertEqual(self.bob.phone_number, '999')
        self.bob.name = 'Ben'
        self.bob.phone_number = '112'
        self.assertNotEqual(self.bob.name, 'Bob')
        self.assertNotEqual(self.bob.phone_number, '999')
        self.assertEqual(self.bob.name, 'Ben')
        self.assertEqual(self.bob.phone_number, '112')

    def testEmailPhone(self):
        self.bob.phone_number = '999'
        self.assertEqual(self.bob.email, '')
        self.assertEqual(self.bob.phone_number, '999')
        self.bob.email = 'bob@a.com'
        self.bob.phone_number = '112'
        self.assertNotEqual(self.bob.phone_number, '999')
        self.assertEqual(self.bob.email, 'bob@a.com')
        self.assertEqual(self.bob.phone_number, '112')

    def testBlacklistedDates(self):
        test_date_1 = date(2012, 12, 31)
        test_date_2 = date(2011, 12, 31)
        self.bob.clear_blacklist()
        self.assertEqual(len(self.bob.blacklisted_dates()), 0)
        self.bob.blacklist_date(test_date_1)
        self.assertEqual(len(self.bob.blacklisted_dates()), 1)
        self.bob.blacklist_date(test_date_2)
        self.assertEqual(len(self.bob.blacklisted_dates()), 2)
        self.bob.blacklist_date(test_date_2)
        self.assertEqual(len(self.bob.blacklisted_dates()), 2)
        self.bob.clear_blacklist()
        self.assertEqual(len(self.bob.blacklisted_dates()), 0)
        self.bob.blacklist_date(test_date_1)
        self.bob.blacklist_date(test_date_2)
        self.assertEqual(len(self.bob.blacklisted_dates()), 2)
        self.bob.free_date(test_date_1)
        self.assertEqual(len(self.bob.blacklisted_dates()), 1)
        self.bob.free_date(test_date_1)
        self.assertEqual(len(self.bob.blacklisted_dates()), 1)
        self.bob.free_date(test_date_2)
        self.assertEqual(len(self.bob.blacklisted_dates()), 0)
        self.bob.free_date(test_date_2)
        self.assertEqual(len(self.bob.blacklisted_dates()), 0)

    def testAvailableDates(self):
        test_date_1 = date(2012, 12, 31)
        test_date_2 = date(2011, 12, 31)
        self.bob.clear_blacklist()
        self.bob.blacklist_date(test_date_1)
        self.assertTrue(self.bob.is_available_on_date(test_date_2))
        self.assertFalse(self.bob.is_available_on_date(test_date_1))
        self.bob.blacklist_date(test_date_2)
        self.assertFalse(self.bob.is_available_on_date(test_date_2))
        self.assertFalse(self.bob.is_available_on_date(test_date_1))
        self.bob.free_date(test_date_1)
        self.assertEqual(len(self.bob.blacklisted_dates()), 1)
        self.assertFalse(self.bob.is_available_on_date(test_date_2))
        self.assertTrue(self.bob.is_available_on_date(test_date_1))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()