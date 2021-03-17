import unittest
from sprint_1 import list_deceased, is_age_legal
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


if __name__ == '__main__':
    """ Run test cases on startup """
    unittest.main(exit=False, verbosity=2)
