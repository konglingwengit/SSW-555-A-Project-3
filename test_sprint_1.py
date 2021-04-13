import unittest
from sprint_1 import *
from prettytable import PrettyTable
from unittest.mock import MagicMock as Mock, patch
import sprint_1

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

    def test_birth_before_death(self):
        """ Test if there both have birth date and death date, birth is before death """
        list_log = []
        self.assertListEqual(birth_before_death(), list_log)

    def test_divorce_before_death(self):
        """ Test if there both have divorce date and death date, divorce is before death """
        list_log = []
        self.assertListEqual(divorce_before_death(), list_log)

    def test_siblingsnotmarry(self):
        """ Test if Sibling was married one another sibling"""
        list_log = []
        self.assertListEqual(siblingsnotmarry(), list_log)
    def test_list_recent_births(self):
        """ Test if List all people in a GEDCOM file who were born in the last 30 days"""
        list_log = []
        self.assertListEqual(list_recent_births(), list_log)
    #
    # def test_unique_birthday(self):
    #     list_log = []
    #     self.assertListEqual(unique_birthday(), list_log)
    # def test_unique_ID(self):
    #     list_log = []
    #     self.assertListEqual(unique_ID(), list_log)
    # User_Story_30: List all living married people in a GEDCOM file
    # Success test
    # @mock.patch("sprint4.printTable")
    def test_list_living_married_individuals_success(self):
        allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Spouse"]
        tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT", "SPOUSE"]
        current_dic = {}
        self.assertListEqual(["US30: Living & Married People Table", allFields, tagNames, current_dic],
                             listLivingMarried())

    def test_less_than_15_siblings(self):
        self.assertEqual(len(anomaly_array), 0)

if __name__ == '__main__':
    """ Run test cases on startup """
    unittest.main(exit=False, verbosity=2)
