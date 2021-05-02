import unittest
from prettytable import PrettyTable
from unittest.mock import MagicMock as Mock, patch
import sprint_4


class TestSprint1(unittest.TestCase):


    def test_date_bef_now(self):
        """ Test all date is before now """
        self.assertEqual(sprint_4.validate_dates(), 0)


    def test_bir_bef_mar(self):
        """ Test if there both have birth date and marriage date, birth is before marriage """
        self.assertEqual(sprint_4.is_birth_before_marraige(), 0)


    def test_birth_before_death(self):
        """ Test if there both have birth date and death date, birth is before death """
        self.assertEqual(sprint_4.birth_before_death(), 0)

    def test_List_Deceased_success(self):
        """Test Case for user story 29"""
        self.assertTrue(sprint_4.list_deceased(), (
            'US29: Deceased People Table', ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death'],
            ['INDI', 'NAME', 'SEX', 'BIRT', 'AGE', 'ALIVE', 'DEAT'], {})
                        )

    def test_is_age_legal(self):
        """as all ages of all persons are legal"""
        self.assertListEqual(sprint_4.is_age_legal(), [])

    def test_birth_before_marriage_of_parents(self):
        self.assertEqual(sprint_4.birth_before_marriage_of_parents(), 0)

    def test_is_marriage_before_divorce(self):
        self.assertEqual(sprint_4.is_marriage_after_divorce(), 0)

    def test_is_marriage_after_death(self):
        self.assertEqual(sprint_4.is_marriage_after_death(), 0)

    def test_list_recent_deaths(self):
        self.assertEqual(sprint_4.list_recent_deaths(), 0)

    def test_list_upcoming_birthday(self):
        self.assertEqual(sprint_4.list_upcoming_birthday(), True)

    def test_list_recent_survivors(self):
        self.assertEqual(sprint_4.list_recent_survivors(), 0)

    def test_divorce_before_death(self):
        """ Test if there both have divorce date and death date, divorce is before death """
        self.assertEqual(sprint_4.check_divorce_before_death(), 0)

    def test_siblingsnotmarry(self):
        """ Test if Sibling was married one another sibling"""
        self.assertEqual(sprint_4.check_sibling_marriage(), 1)

    def test_list_recent_births(self):
        """ Test if List all people in a GEDCOM file who were born in the last 30 days"""
        self.assertEqual(sprint_4.list_recent_births(), True)

    def test_parents_not_old(self):
        self.assertEqual(sprint_4.parents_not_old(), 0)

    def test_siblings_spacing(self):
        self.assertEqual(sprint_4.siblings_spacing(), 1)

    def test_listOrphans(self):
        self.assertEqual(sprint_4.listOrphans(), True)

    def test_accpet_partial_dates(self):
        self.assertEqual(sprint_4.accpet_partial_dates(), None)

    #
    def test_unique_birthday(self):
        self.assertEqual(sprint_4.unique_birthday(), 1)

    def test_unique_ID(self):
        self.assertEqual(sprint_4.unique_ID(), 1)

    def test_list_living_married_individuals_success(self):
        self.assertEqual(len(sprint_4.listLivingMarried()), 4)

    def test_less_than_15_siblings(self):
        self.assertEqual(len(sprint_4.anomaly_array), 0)

    def test_large_age_diff(self):
        self.assertEqual(len(sprint_4.large_age_diff()), 0)

    def test_valid_dates_fail(self):
        error_array = []
        sprint_4.validate_date()
        self.assertIsInstance(error_array, type(sprint_4.validate_date()))

    def test_list_upcoming_anni_pass(self):
        """ Test case for US39 (pass) """
        self.assertTrue(sprint_4.list_upcoming_anni(), True)

    def test_check_last_names(self):
        self.assertEqual(sprint_4.check_last_names(), 1)

    def test_is_uncle_aunt_marriage_legal(self):
        self.assertEqual(sprint_4.is_uncle_aunt_marriage_legal(), True)

    def test_check_sibling_count(self):
        self.assertEqual(sprint_4.check_sibling_count(), 0)

    def test_check_multiple_births(self):
        self.assertEqual(sprint_4.check_multiple_births(), 1)

    def test_check_for_bigamy(self):
        sprint_4.create_family_dic()
        self.assertEqual(sprint_4.check_for_bigamy(), 1)

    def test_birth_before_death_pass(self):
        """ Test code for US09 (pass) """
        sprint_4.error_array = []
        sprint_4.birth_before_death_parents()
        self.assertEqual(len(sprint_4.error_array), 0)

    def test_unique_family_by_spouses(self):
        self.assertEqual(sprint_4.unique_family_by_spouses(), 1)

    def test_is_marriage_legal(self):
        self.assertEqual(sprint_4.is_marriage_legal(), 0)

    def test_check_positive_parent_child_marriage(self):
        family_dic = {'@F1@': {'HUSB': '@I1@', 'WIFE': '@I2@', 'FAM_CHILD': ['@I3@']},
                      '@F2@': {'HUSB': '@I3@', 'WIFE': '@I2@', 'WIFE_LINE': '11'}}
        individuals = {'@I1@': {'SPOUSE': ['@F1@']}, '@I2@': {'SPOUSE': ['@F1@', '@F2@']}, '@I3@': {'SPOUSE': ['@F2@']}}

        temp_family_dic = sprint_4.family_dic
        temp_individuals = sprint_4.individuals

        sprint_4.family_dic = family_dic
        sprint_4.anomaly_array = []
        sprint_4.individuals = individuals
        sprint_4.check_parent_child_marriage()

        self.assertEqual(sprint_4.anomaly_array[0], "ANOMALY: INDIVIDUAL: US17: 11: @I2@: Individual married to child "
                                                    "@I3@")
        sprint_4.individuals = temp_individuals
        sprint_4.family_dic = temp_family_dic
        sprint_4.anomaly_array = []

    def test_list_nomarried_living(self):
        self.assertEqual(sprint_4.list_nomarried_living(), True)

    def test_family_gender_fail(self):
        sprint_4.error_array = []
        sprint_4.correct_gender()
        self.assertEqual(sprint_4.error_array, [])

    def test_unique_family_name_and_birth(self):
        self.assertEqual(sprint_4.unique_family_name_and_birth(), 1)

    def test_include_age(self):
        test_dict = {'@I1@': {'AGE': 42,
                              'ALIVE': True,
                              'BIRT': '1978 - 8 - 18',
                              'BIRT_LINE': 20,
                              'DEAT': 'NA',
                              'FAMC_LINE': 22,
                              'INDI': '@I1@',
                              'INDI_CHILD': ['@F1@'],
                              'INDI_LINE': 14,
                              'NAME': 'Nicholas /Mike/',
                              'NAME_LINE': 15,
                              'SEX': 'M',
                              'SEX_LINE': 19,
                              'SPOUSE': 'NA'},
                     '@I2@': {'AGE': 70,
                              'ALIVE': True,
                              'BIRT': '1950 - 11 - 11',
                              'BIRT_LINE': 29,
                              'DEAT': 'NA',
                              'FAMS_LINE': 32,
                              'INDI': '@I2@',
                              'INDI_CHILD': 'NA',
                              'INDI_LINE': 23,
                              'NAME': 'Jason /Mike/',
                              'NAME_LINE': 24,
                              'SEX': 'M',
                              'SEX_LINE': 28,
                              'SPOUSE': ['@F1@', '@F3@']},
                     '@I3@': {'AGE': 70,
                              'ALIVE': False,
                              'BIRT': '1950 - 11 - 11',
                              'BIRT_LINE': 39,
                              'DEAT': '2021 - 3 - 24',
                              'DEAT_LINE': 41,
                              'FAMS_LINE': 43,
                              'INDI': '@I3@',
                              'INDI_CHILD': 'NA',
                              'INDI_LINE': 33,
                              'NAME': 'Nancy /Leo/',
                              'NAME_LINE': 34,
                              'SEX': 'F',
                              'SEX_LINE': 38,
                              'SPOUSE': ['@F1@']},
                     '@I4@': {'AGE': 30,
                              'ALIVE': True,
                              'BIRT': '1990 - 6 - 30',
                              'BIRT_LINE': 50,
                              'DEAT': 'NA',
                              'FAMC_LINE': 54,
                              'FAMS_LINE': 53,
                              'INDI': '@I4@',
                              'INDI_CHILD': ['@F3@'],
                              'INDI_LINE': 44,
                              'NAME': 'Ilia /Mike/',
                              'NAME_LINE': 45,
                              'SEX': 'M',
                              'SEX_LINE': 49,
                              'SPOUSE': ['@F2@', '@F4@']},
                     '@I5@': {'AGE': 60,
                              'ALIVE': True,
                              'BIRT': '1960 - 10 - 16',
                              'BIRT_LINE': 61,
                              'DEAT': 'NA',
                              'FAMS_LINE': 63,
                              'INDI': '@I5@',
                              'INDI_CHILD': 'NA',
                              'INDI_LINE': 55,
                              'NAME': 'Claire /John/',
                              'NAME_LINE': 56,
                              'SEX': 'F',
                              'SEX_LINE': 60,
                              'SPOUSE': ['@F3@']},
                     '@I6@': {'AGE': 2,
                              'ALIVE': True,
                              'BIRT': '2018 - 7 - 23',
                              'BIRT_LINE': 70,
                              'DEAT': 'NA',
                              'FAMC_LINE': 72,
                              'INDI': '@I6@',
                              'INDI_CHILD': ['@F2@'],
                              'INDI_LINE': 64,
                              'NAME': 'Jerry /Mike/',
                              'NAME_LINE': 65,
                              'SEX': 'M',
                              'SEX_LINE': 69,
                              'SPOUSE': 'NA'},
                     '@I7@': {'AGE': 27,
                              'ALIVE': True,
                              'BIRT': '1993 - 7 - 20',
                              'BIRT_LINE': 80,
                              'DEAT': 'NA',
                              'FAMS_LINE': 82,
                              'INDI': '@I7@',
                              'INDI_CHILD': 'NA',
                              'INDI_LINE': 74,
                              'NAME': 'Yvette /Dwight/',
                              'NAME_LINE': 75,
                              'SEX': 'F',
                              'SEX_LINE': 79,
                              'SPOUSE': ['@F2@']},
                     '@I8@': {'AGE': 0,
                              'ALIVE': True,
                              'BIRT': '2021 - 2 - 10',
                              'BIRT_LINE': 89,
                              'DEAT': 'NA',
                              'FAMC_LINE': 91,
                              'INDI': '@I8@',
                              'INDI_CHILD': ['@F4@'],
                              'INDI_LINE': 83,
                              'NAME': 'Horford /Mike/',
                              'NAME_LINE': 84,
                              'SEX': 'M',
                              'SEX_LINE': 88,
                              'SPOUSE': 'NA'},
                     '@I9@': {'AGE': 26,
                              'ALIVE': True,
                              'BIRT': '1994 - 8 - 14',
                              'BIRT_LINE': 98,
                              'DEAT': 'NA',
                              'FAMS_LINE': 100,
                              'INDI': '@I9@',
                              'INDI_CHILD': 'NA',
                              'INDI_LINE': 92,
                              'NAME': 'Jennifer /James/',
                              'NAME_LINE': 93,
                              'SEX': 'F',
                              'SEX_LINE': 97,
                              'SPOUSE': ['@F4@']}}
        self.assertEqual(sprint_4.include_individual_ages(), test_dict)

    def test_list_siblings_by_age_success(self):
        self.assertEqual(sprint_4.listSiblingsByAge(), 0)

    def test_list_siblings_by_age_success(self):
        self.assertEqual(sprint_4.listSiblingsByAge(), 0)

    def test_multiple_birth(self):
        self.assertEqual(sprint_4.multiple_birth_same(),
                         [])

    def test_include_line_number(self):
        sprint_4.include_line_number("test")
        self.assertEqual(sprint_4.individuals['@I6@']['LINE_NUMBER'], '64')


if __name__ == '__main__':
    """ Run test cases on startup """
    unittest.main(exit=False, verbosity=2)
