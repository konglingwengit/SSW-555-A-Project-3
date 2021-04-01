import unittest
from sprint_1 import list_deceased, is_age_legal, unique_ID
from sprint_1 import bir_bef_mar, date_bef_now, unique_birthday
from prettytable import PrettyTable
from unittest.mock import MagicMock as Mock, patch


class TestSprint1(unittest.TestCase):

    def test_List_Deceased_success(self):
        """Test Case for user story 29"""
        self.assertTrue(list_deceased(), (
            'US29: Deceased People Table', ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death'],
            ['INDI', 'NAME', 'SEX', 'BIRT', 'AGE', 'ALIVE', 'DEAT'], {})
                        )

    def test_is_age_legal(self):
        """as all ages of all persons are legal"""
        lst = []
        self.assertListEqual(is_age_legal(), lst)

    def test_date_bef_now(self):
        """ Test all date is before now """
        list_log = []
        self.assertListEqual(date_bef_now(), list_log)

    def test_bir_bef_mar(self):
        """ Test if there both have birth date and marriage date, birth is before marriage """
        list_log = []
        self.assertListEqual(bir_bef_mar(), list_log)
    def test_unique_birthday(self):
        list_log = []
        self.assertListEqual(unique_birthday(), list_log)
    def test_unique_ID(self):
        list_log = []
        self.assertListEqual(unique_ID(), list_log)

if __name__ == '__main__':
    """ Run test cases on startup """
    unittest.main(exit=False, verbosity=2)
