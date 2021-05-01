import unittest
from prettytable import PrettyTable
from unittest.mock import MagicMock as Mock, patch
import sprint_1


class TestSprint1(unittest.TestCase):

    def test_List_Deceased_success(self):
        """Test Case for user story 29"""
        self.assertTrue(sprint_1.list_deceased(), (
            'US29: Deceased People Table', ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death'],
            ['INDI', 'NAME', 'SEX', 'BIRT', 'AGE', 'ALIVE', 'DEAT'], {})
                        )

    def test_is_age_legal(self):
        """as all ages of all persons are legal"""
        lst = []
        self.assertListEqual(sprint_1.is_age_legal(), lst)

    def test_date_bef_now(self):
        """ Test all date is before now """
        self.assertEqual(sprint_1.date_bef_now(), None)

    def test_bir_bef_mar(self):
        """ Test if there both have birth date and marriage date, birth is before marriage """
        self.assertEqual(sprint_1.bir_bef_mar(), None)

    def test_mar_bef_div(self):
        """ Test if there both have marriage date and divorce date, marriage is before divorce """
        self.assertEqual(sprint_1.divorce_before_death(), None)

    def test_birth_before_death(self):
        """ Test if there both have birth date and death date, birth is before death """
        self.assertEqual(sprint_1.birth_before_death(), None)

    def test_divorce_before_death(self):
        """ Test if there both have divorce date and death date, divorce is before death """
        self.assertEqual(sprint_1.divorce_before_death(), None)

    def test_siblingsnotmarry(self):
        """ Test if Sibling was married one another sibling"""
        self.assertEqual(sprint_1.siblingsnotmarry(), None)

    def test_list_recent_births(self):
        """ Test if List all people in a GEDCOM file who were born in the last 30 days"""
        self.assertEqual(sprint_1.list_recent_births(), None)

    def test_parents_not_old(self):
        self.assertEqual(sprint_1.parents_not_old(), None)

    def test_siblings_spacing(self):
        self.assertEqual(sprint_1.siblings_spacing(), [])

    def test_listOrphans(self):
        self.assertEqual(sprint_1.listOrphans(), None)

    def test_accpet_partial_dates(self):
        self.assertEqual(sprint_1.accpet_partial_dates(), None)

    #
    def test_unique_birthday(self):
        self.assertEqual(sprint_1.unique_birthday(), None)

    def test_unique_ID(self):
        self.assertEqual(sprint_1.unique_ID(), None)

    # User_Story_30: List all living married people in a GEDCOM file
    # Success test
    # @mock.patch("sprint4.printTable")
    def test_list_living_married_individuals_success(self):
        self.assertListEqual(sprint_1.listLivingMarried(), ['US30: Living & Married People Table',
                                                            ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive',
                                                             'Death', 'Spouse'],
                                                            ['INDI', 'NAME', 'SEX', 'BIRT', 'AGE', 'ALIVE', 'DEAT',
                                                             'SPOUSE'], {
                                                                '@I1@': {'INDI': '@I1@', 'NAME': 'Nicholas /Mike/',
                                                                         'SEX': 'M', 'BIRT': '1978 - 8 - 18',
                                                                         'INDI_CHILD': ['F1'], 'SPOUSE': ['NA'],
                                                                         'DEAT': 'NA', 'AGE': 42, 'ALIVE': True},
                                                                '@I2@': {'INDI': '@I2@', 'NAME': 'Jason /Mike/',
                                                                         'SEX': 'M', 'BIRT': '1950 - 11 - 11',
                                                                         'INDI_CHILD': ['NA'], 'SPOUSE': ['F1', 'F3'],
                                                                         'DEAT': 'NA', 'AGE': 70, 'ALIVE': True},
                                                                '@I4@': {'INDI': '@I4@', 'NAME': 'Ilia /Mike/',
                                                                         'SEX': 'M', 'BIRT': '1990 - 6 - 30',
                                                                         'INDI_CHILD': ['F3'], 'SPOUSE': ['F2', 'F4'],
                                                                         'DEAT': 'NA', 'AGE': 30, 'ALIVE': True},
                                                                '@I5@': {'INDI': '@I5@', 'NAME': 'Claire /John/',
                                                                         'SEX': 'F', 'BIRT': '1960 - 10 - 16',
                                                                         'INDI_CHILD': ['NA'], 'SPOUSE': ['F3'],
                                                                         'DEAT': 'NA', 'AGE': 60, 'ALIVE': True},
                                                                '@I6@': {'INDI': '@I6@', 'NAME': 'Jerry /Mike/',
                                                                         'SEX': 'M', 'BIRT': '2018 - 7 - 23',
                                                                         'INDI_CHILD': ['F2'], 'SPOUSE': ['NA'],
                                                                         'DEAT': 'NA', 'AGE': 2, 'ALIVE': True},
                                                                '@I7@': {'INDI': '@I7@', 'NAME': 'Yvette /Dwight/',
                                                                         'SEX': 'F', 'BIRT': '1993 - 7 - 20',
                                                                         'INDI_CHILD': ['NA'], 'SPOUSE': ['F2'],
                                                                         'DEAT': 'NA', 'AGE': 27, 'ALIVE': True},
                                                                '@I8@': {'INDI': '@I8@', 'NAME': 'Horford /Mike/',
                                                                         'SEX': 'M', 'BIRT': '2021 - 2 - 10',
                                                                         'INDI_CHILD': ['F4'], 'SPOUSE': ['NA'],
                                                                         'DEAT': 'NA', 'AGE': 0, 'ALIVE': True},
                                                                '@I9@': {'INDI': '@I9@', 'NAME': 'Jennifer /James/',
                                                                         'SEX': 'F', 'BIRT': '1994 - 8 - 14',
                                                                         'INDI_CHILD': ['NA'], 'SPOUSE': ['F4'],
                                                                         'DEAT': 'NA', 'AGE': 26, 'ALIVE': True}}])

    def test_less_than_15_siblings(self):
        self.assertEqual(len(sprint_1.anomaly_array), 0)

    def test_large_age_diff(self):
        self.assertEqual(len(sprint_1.anomaly_array), 0)

    def test_is_marriage_before_divorce(self):
        self.assertEqual(len(sprint_1.is_marriage_before_divorce()), 0)

    # US42
    def test_valid_dates_fail(self):
        error_array = []
        sprint_1.validate_date()
        self.assertIsInstance(error_array, type(sprint_1.validate_date()))

    # US39
    # lingwen Kong
    def test_list_upcoming_anni_pass(self):
        """ Test case for US39 (pass) """
        self.assertTrue(sprint_1.list_upcoming_anni(), True)

    def test_birth_before_death_pass(self):
        """ Test code for US09 (pass) """
        sprint_1.error_array = []
        sprint_1.birth_before_death_parents()
        self.assertEqual(len(sprint_1.error_array), 0)

    def test_check_positive_parent_child_marriage(self):
        family_dic = {'@F1@': {'HUSB': '@I1@', 'WIFE': '@I2@', 'FAM_CHILD': ['@I3@']},
                      '@F2@': {'HUSB': '@I3@', 'WIFE': '@I2@', 'WIFE_LINE': '11'}}
        individuals = {'@I1@': {'SPOUSE': ['@F1@']}, '@I2@': {'SPOUSE': ['@F1@', '@F2@']}, '@I3@': {'SPOUSE': ['@F2@']}}

        temp_family_dic = sprint_1.family_dic
        temp_individuals = sprint_1.individuals

        sprint_1.family_dic = family_dic
        sprint_1.anomaly_array = []
        sprint_1.individuals = individuals
        sprint_1.check_parent_child_marriage()

        self.assertEqual(sprint_1.anomaly_array[0], "ANOMALY: INDIVIDUAL: US17: 11: @I2@: Individual married to child "
                                                    "@I3@")
        sprint_1.individuals = temp_individuals
        sprint_1.family_dic = temp_family_dic
        sprint_1.anomaly_array = []

    def test_family_gender_fail(self):
        sprint_1.error_array = []
        sprint_1.correct_gender()
        self.assertEqual(sprint_1.error_array, [])



    # US27
    def test_include_age(self):
        test_dict = {'@I1@': {'INDI': '@I1@', 'NAME': 'Nicholas /Mike/', 'SEX': 'M', 'BIRT': '1978 - 8 - 18',
                              'INDI_CHILD': ['F1'], 'SPOUSE': ['NA'], 'DEAT': 'NA', 'AGE': 42, 'ALIVE': True},
                     '@I2@': {'INDI': '@I2@', 'NAME': 'Jason /Mike/', 'SEX': 'M', 'BIRT': '1950 - 11 - 11',
                              'INDI_CHILD': ['NA'], 'SPOUSE': ['F1', 'F3'], 'DEAT': 'NA', 'AGE': 70, 'ALIVE': True},
                     '@I3@': {'INDI': '@I3@', 'NAME': 'Nancy /Leo/', 'SEX': 'F', 'BIRT': '1950 - 11 - 11',
                              'DEAT': '2021 - 3 - 24', 'INDI_CHILD': ['NA'], 'SPOUSE': ['F1'], 'AGE': 70,
                              'ALIVE': False},
                     '@I4@': {'INDI': '@I4@', 'NAME': 'Ilia /Mike/', 'SEX': 'M', 'BIRT': '1990 - 6 - 30',
                              'INDI_CHILD': ['F3'], 'SPOUSE': ['F2', 'F4'], 'DEAT': 'NA', 'AGE': 30, 'ALIVE': True},
                     '@I5@': {'INDI': '@I5@', 'NAME': 'Claire /John/', 'SEX': 'F', 'BIRT': '1960 - 10 - 16',
                              'INDI_CHILD': ['NA'], 'SPOUSE': ['F3'], 'DEAT': 'NA', 'AGE': 60, 'ALIVE': True},
                     '@I6@': {'INDI': '@I6@', 'NAME': 'Jerry /Mike/', 'SEX': 'M', 'BIRT': '2018 - 7 - 23',
                              'INDI_CHILD': ['F2'], 'SPOUSE': ['NA'], 'DEAT': 'NA', 'AGE': 2, 'ALIVE': True},
                     '@I7@': {'INDI': '@I7@', 'NAME': 'Yvette /Dwight/', 'SEX': 'F', 'BIRT': '1993 - 7 - 20',
                              'INDI_CHILD': ['NA'], 'SPOUSE': ['F2'], 'DEAT': 'NA', 'AGE': 27, 'ALIVE': True},
                     '@I8@': {'INDI': '@I8@', 'NAME': 'Horford /Mike/', 'SEX': 'M', 'BIRT': '2021 - 2 - 10',
                              'INDI_CHILD': ['F4'], 'SPOUSE': ['NA'], 'DEAT': 'NA', 'AGE': 0, 'ALIVE': True},
                     '@I9@': {'INDI': '@I9@', 'NAME': 'Jennifer /James/', 'SEX': 'F', 'BIRT': '1994 - 8 - 14',
                              'INDI_CHILD': ['NA'], 'SPOUSE': ['F4'], 'DEAT': 'NA', 'AGE': 26, 'ALIVE': True}}
        self.assertEqual(sprint_1.include_individual_ages(), test_dict)

    def test_list_siblings_by_age_success(self):
        self.assertEqual(sprint_1.listSiblingsByAge(), 0)

    def test_list_siblings_by_age_success(self):
        self.assertEqual(sprint_1.listSiblingsByAge(), 0)

    def test_multiple_birth(self):
        self.assertEqual(sprint_1.multiple_birth_same(),
                         [])


if __name__ == '__main__':
    """ Run test cases on startup """
    unittest.main(exit=False, verbosity=2)
