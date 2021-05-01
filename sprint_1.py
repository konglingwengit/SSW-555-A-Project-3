from datetime import datetime, time, timedelta, date
from typing import Dict, Any, List
from prettytable import PrettyTable

defined_tag: List[str] = ["INDI", "FAM"]
header_tags_list = ["HEAD", "TRLR", "NOTE"]
tags_list = ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "DIV", "HUSB", "WIFE", "CHIL"]
tags_dict: Dict = {"INDI": ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS"],
                   "FAM": ["MARR", "DIV", "HUSB", "WIFE", "CHIL"],
                   "DATE": ["BIRT", "DEAT", "DIV", "MARR"]}

family_dic = {}
anomaly_array = []
ged_data = {}
individuals: Dict[Any, Any] = {}
error_array = []


def create_individuals_map():
    global individuals
    individuals = {}

    for individual in ged_data["INDI"]:
        individuals[individual["INDI"]] = individual


def create_family_dic():
    global family_dic
    family_dic = {}

    for family in ged_data["FAM"]:
        if family["HUSB"] != "NA" and family["HUSB"] in individuals:
            family["husband_object"] = individuals[family["HUSB"]]

        if family["WIFE"] != "NA" and family["WIFE"] in individuals:
            family["wife_object"] = individuals[family["WIFE"]]

        if family["FAM_CHILD"] != "NA":
            children = []
            for child in family["FAM_CHILD"]:
                try:
                    children.append(individuals[child])
                except:
                    pass
            family["children_objects"] = children

        family_dic[family["FAM"]] = family


# create_family_dic()
def get_month_num(shortMonth):
    """:returns general number of given month"""
    return {
        'JAN': "1",
        'FEB': "2",
        'MAR': "3",
        'APR': "4",
        'MAY': "5",
        'JUN': "6",
        'JUL': "7",
        'AUG': "8",
        'SEP': "9",
        'OCT': "10",
        'NOV': "11",
        'DEC': "12"
    }[shortMonth]


# converts date
def format_date(date_arr):
    return f'{date_arr[2]} - {get_month_num(date_arr[1])} - {date_arr[0]}'


# find age based on birth & death date
def determine_age(birth_date, death_date):
    if death_date:
        return int(death_date.split('-')[0]) - int(birth_date.split('-')[0])
    else:
        today = datetime.today()
        return today.year - int(birth_date.split('-')[0])


# Prints out a table from dictionary
def print_table(table_name, fields, tag_names, dictionary):
    """prints table according to assignment document"""
    print(table_name)
    table = PrettyTable()
    table.field_names = fields
    for element in dictionary.values():
        count = 1
        row_data = ""  # string uses to store each tag within the current element
        for name in tag_names:
            if count < int(len(tag_names)):  # not the last element
                if isinstance(element[name], list):  # current element is an array
                    row_data += (",".join(element[name]) + "? ")
                else:  # current element is not an array
                    row_data += (str(element[name]) + "? ")
            elif count == int(len(tag_names)):
                if isinstance(element[name], list):  # current element is an array
                    row_data += (",".join(element[name]))
                else:  # current element is not an array
                    row_data += (str(element[name]))
                break
            count += 1
        table.add_row(row_data.split('?'))
    print(table)


def find_name(arr, _id):
    for indi in arr:
        if _id == indi["INDI"]:
            return indi["NAME"]


def read_ged_data(file):
    """:returns dictionary of list of individuals"""
    doc = {"INDI": [], "FAM": []}
    dic = {}
    flag = False

    with open(file) as file_p:
        all_lines = file_p.readlines()
        for line, next_line in zip(all_lines, all_lines[1:]):
            current_arr = line.strip().split(" ")
            next_arr = next_line.strip().split(" ")

            if len(current_arr) == 3 and current_arr[0] == '0' and current_arr[2] == "INDI":
                current_tag = "INDI"
                dic = {"INDI": current_arr[1]}
            elif len(current_arr) == 3 and current_arr[0] == '0' and current_arr[2] == "FAM":
                current_tag = "FAM"
                dic = {"FAM": current_arr[1]}
            elif current_arr[1] == "DATE" and flag:
                flag = False
                date_arr = current_arr[2:]
                dic[tmp] = format_date(date_arr)
            elif current_arr[0] == '1' and current_arr[1] in tags_list:
                if current_arr[1] in tags_dict["DATE"]:
                    tmp = current_arr[1]
                    flag = True
                else:
                    if current_arr[1] == "HUSB":
                        individual_husband = find_name(doc["INDI"], current_arr[2])
                        dic["HUSB_NAME"] = individual_husband
                    if current_arr[1] == "WIFE":
                        individual_husband = find_name(doc["INDI"], current_arr[2])
                        dic["WIFE_NAME"] = individual_husband
                    if current_arr[1] == 'CHIL':
                        children = dic["FAM_CHILD"] if "FAM_CHILD" in dic else []
                        children.append(f"{current_arr[2].strip('@')}")
                        dic["FAM_CHILD"] = children
                    if current_arr[1] == 'FAMC' or current_arr[1] == 'FAMS':
                        child = dic["INDI_CHILD"] if "INDI_CHILD" in dic else []
                        spouse = dic["SPOUSE"] if "SPOUSE" in dic else []
                        if current_arr[1] == 'FAMC':
                            child.append(f"{current_arr[2].strip('@')}")
                        if current_arr[1] == 'FAMS':
                            spouse.append(f"{current_arr[2].strip('@')}")
                        dic['INDI_CHILD'] = child
                        dic['SPOUSE'] = spouse
                    else:
                        dic[current_arr[1]] = ' '.join(current_arr[2:])

            if (len(next_arr) == 3 and next_arr[0] == '0' and next_arr[2] in defined_tag) or next_arr[1] == "TRLR":
                if dic:
                    if current_tag == 'INDI':
                        if 'DEAT' in dic:
                            age = determine_age(dic['BIRT'], dic['DEAT'])
                            alive = False
                        else:
                            age = determine_age(dic['BIRT'], None)
                            alive = True
                            dic['DEAT'] = 'NA'
                        dic["AGE"] = str(age)
                        dic['ALIVE'] = alive

                        if not dic["SPOUSE"]:
                            dic["SPOUSE"] = ["NA"]
                        elif not dic["INDI_CHILD"]:
                            dic["INDI_CHILD"] = ["NA"]

                    if current_tag == 'FAM':
                        if "DIV" not in dic:
                            dic["DIV"] = ["NA"]
                        if "HUSB" not in dic:
                            dic["HUSB"] = ["NA"]
                        if "HUSB_NAME" not in dic:
                            dic["HUSB_NAME"] = ["NA"]
                        if "WIFE" not in dic:
                            dic["WIFE"] = ["NA"]
                        if "WIFE_NAME" not in dic:
                            dic["WIFE_NAME"] = ["NA"]
                        if "FAM_CHILD" not in dic:
                            dic["FAM_CHILD"] = ["NA"]
                        if "MARR" not in dic:
                            dic["MARR"] = ["NA"]

                    doc[current_tag].append(dic)

        return doc


ged_data = read_ged_data("test_data.ged")
create_individuals_map()


# US29: List all deceased individuals in a GEDCOM file
# Prints deceased people's list
# Lingweng Kong
def list_deceased():
    """Prints deceased people's list"""
    current_dic = {}
    print("User_Story_29: List all deceased individuals in a GEDCOM file")
    for value in individuals.values():
        if str(value["DEAT"]) != "NA" and (value["ALIVE"]):
            anomaly_array.append(
                "ERROR: INDIVIDUAL: US29: {}: Person is alive but has Death Date {}".format(value["NAME"],
                                                                                            value["DEAT"]))
            print("ERROR: INDIVIDUAL: US29: Person {} is alive but has Death Date {}".format(value["NAME"],
                                                                                             value["DEAT"]))
        elif str(value["DEAT"]) == "NA" and (not value["ALIVE"]):
            anomaly_array.append(
                "ERROR: INDIVIDUAL: US29: {}: Person is dead but has no Death Date".format(value["DEAT"]))
            print("ERROR: INDIVIDUAL: US29: {}: Person is dead but has no Death Date".format(value["INDI"]))
        elif not value["ALIVE"]:
            current_dic[value["INDI"]] = value
            # Use pretty table module to print out the results
    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT"]
    print_table("US29: Deceased People Table", allFields, tagNames, current_dic)
    return "US29: Deceased People Table", allFields, tagNames, current_dic


# US07: Death should be less than 150 years after birth for dead people, and current date should be less than 150
# years after birth for all living people
# Less then 150 years old
# Lingweng Kong
def is_age_legal():
    """ Less then 150 years old """
    for indivisual_id in individuals:
        indi = individuals[indivisual_id]

        if "AGE" in indi:
            age = indi["AGE"]

            if int(age) > 150:
                if indi["ALIVE"]:
                    anomaly_array.append(
                        "ANOMALY: INDIVIDUAL: US07: {indivisual_id}:"
                        " More than 150 years old - Birth Date {indi['BIRT']}")
                else:
                    anomaly_array.append(
                        "ANOMALY: INDIVIDUAL: US07: {indivisual_id}: More than 150 years old at death"
                        " - Birth Date {indi['BIRT']}: Death Date {indi['DEAT']}")
    return anomaly_array


# US01: Dates before current date
# Dates (birth, marriage, divorce, death) should not be after the current date
# Hengyuan Zhang
def date_bef_now():
    """ store date in individuals and return error list"""
    for family in family_dic.values():
        if family["MARR"] != "NA":
            if (determine_age(family["MARR"], None) < 0):
                anomaly_array.append(
                    "ERROR: FAMILY: US01: {}: Family has marrige date {} later than today".format(family["FAM"],
                                                                                                  family["MARR"]))
        if family["DIV"] != "NA":
            if (determine_age(family["DIV"], None) < 0):
                anomaly_array.append(
                    "ERROR: FAMILY: US01: {}: Family has divorce date {} later than today".format(family["FAM"],
                                                                                                  family["DIV"]))

    for indi in individuals.values():
        # for birthday simply check age
        if (determine_age(indi["BIRT"], None) < 0):
            anomaly_array.append(
                "ERROR: INDIVIDUAL: US01: {}: Individual has birth date {} later than today".format(indi["INDI"],
                                                                                                    indi["BIRT"]))
        if indi["DEAT"] != "NA":
            if (determine_age(indi["DEAT"], None) < 0):
                anomaly_array.append(
                    "ERROR: INDIVIDUAL: US01: {}: Individual has death date {} later than today".format(indi["INDI"],
                                                                                                        indi["DEAT"]))


def is_date_after(date_one, date_two):
    return date_one < date_two


# US02: Birth before marriage
# Birth should occur before marriage of an individual
# Hengyuan Zhang
def bir_bef_mar():
    for family_id in family_dic:
        family = family_dic[family_id]
        if "MARR" in family:
            marriage_date = family["MARR"]
            husband_birth_date = None
            wife_birth_date = None
            if "husband_object" in family and "BIRT" in family["husband_object"]:
                husband_birth_date = family["husband_object"]["BIRT"]
            else:
                continue
            if "wife_object" in family and "BIRT" in family["wife_object"]:
                wife_birth_date = family["wife_object"]["BIRT"]
            else:
                continue
            if is_date_after(marriage_date, husband_birth_date):
                anomaly_array.append(
                    ("ERROR: INDIVIDUAL: US02: {}: Person has marriage date {} before birth date {}").format(
                        family["husband_object"]["INDI"], marriage_date, husband_birth_date))
            if is_date_after(marriage_date, wife_birth_date):
                anomaly_array.append(
                    ("ERROR: INDIVIDUAL: US02: {}: Person has marriage date {} before birth date {}").format(
                        family["wife_object"]["INDI"], marriage_date, wife_birth_date))


# USO3: Birth before death
# Birth should occur before death of an individual
# Muyang Li
def birth_before_death():
    """ store birth date and death in individuals and return error list"""
    for currentIndividual in individuals.values():
        if (currentIndividual['BIRT'] == 'NA'):
            error_array.append(
                "ERROR: INDIVIDUAL: US03: {}: Individual has no Birth Date".format(currentIndividual["INDI"]))
        elif (currentIndividual['DEAT'] != 'NA'):
            if (currentIndividual['BIRT'] > currentIndividual['DEAT']):
                error_array.append(
                    "ERROR: INDIVIDUAL: US03: {}: Individual has Birth date {} after Death Date {}".format(
                        currentIndividual["INDI"], currentIndividual["BIRT"], currentIndividual["DEAT"]))


# US04: Marriage before divorce
# Marriage should occur before divorce of spouses, and divorce can only occur after marriage
# Hengyuan Zhang
def mar_bef_div():
    """ store marriage and divorce date in individuals and return error list"""
    list_error = []
    for indivisual_id in individuals:
        indi = individuals[indivisual_id]
        if "MARR" in indi and "DIV" in indi:
            mar_date_str = indi["MARR"]
            div_date_str = indi["DIV"]
            mar_date = datetime.datetime.strptime(mar_date_str, '%Y-%m-%d')
            div_date = datetime.datetime.strptime(div_date_str, '%Y-%m-%d')
            if (mar_date - div_date).days >= 0:
                log = indi + "has a inavilable date: Marriage date is after div date."
                list_error.append(log)
        else:
            log = indi + "doesn't have enough date data of Marriage or Divorce."
            list_error.append(log)
    return list_error


# US05: Marriage before death
# Marriage should before death of an individual
# Hengyuan Zhang
def mar_bef_death():
    """ store marriage and death date in individuals and return error list"""
    list_error = []
    for indivisual_id in individuals:
        indi = individuals[indivisual_id]
        if "MARR" in indi and "DEAT" in indi:
            mar_date_str = indi["MARR"]
            death_date_str = indi["DEAT"]
            mar_date = datetime.datetime.strptime(mar_date_str, '%Y-%m-%d')
            death_date = datetime.datetime.strptime(death_date_str, '%Y-%m-%d')
            if (mar_date - death_date).days >= 0:
                log = indi + "has a inavilable date: Marriage date is after death date."
                list_error.append(log)
        else:
            log = indi + "doesn't have enough date data of Marriage and Death."
            list_error.append(log)
    return list_error


# US06: Divorce before death
# Divorce can only occur before death of both spouses
# Muyang Li
def divorce_before_death():
    """ store divorce date and death in individuals and return error list"""
    for family in family_dic.values():
        husband_flag = False
        wife_flag = False
        if "DIV" in family and family["DIV"] != "NA":
            divorce_date = family["DIV"]
            if "husband_object" in family and family["husband_object"] != 'NA':
                husband = family["husband_object"]
                if "DEAT" in husband and husband["DEAT"] != 'NA':
                    husband_flag = True
                    husband_death = husband["DEAT"]
            if "wife_object" in family and family["wife_object"] != 'NA':
                wife = family["wife_object"]
                if "DEAT" in wife and wife["DEAT"] != 'NA':
                    wife_flag = True
                    wife_death = wife["DEAT"]
            if husband_flag and wife_flag:
                husband_invalid = False
                wife_invalid = False
                if determine_days(husband_death, divorce_date) > 0:
                    husband_invalid = True
                if determine_days(wife_death, divorce_date) > 0:
                    wife_invalid = True
                if husband_invalid and wife_invalid:
                    error_array.append(
                        "ERROR: FAMILY: US06: {}: {}: Divorce {} happened after the death of both spouses - Husband: {} Wife: {}.".format(
                            family["DIV_LINE"], family["FAM"], family["DIV"], husband_death, wife_death))
                elif husband_invalid:
                    error_array.append(
                        "ERROR: FAMILY: US06: {}: {}: Divorce {} happened after the death of husband {}.".format(
                            family["DIV_LINE"], family["FAM"], family["DIV"], husband_death, wife_death))
                elif wife_invalid:
                    error_array.append(
                        "ERROR: FAMILY: US06: {}: {}: Divorce {} happened after the death of wife {}.".format(
                            family["DIV_LINE"], family["FAM"], family["DIV"], husband_death, wife_death))


# US08: Birth before marriage of parents
# Children should be born after marriage of parents (and not more than 9 months after their divorce)
# Muyang Li
def birth_before_marriage_of_parents():
    """" store children's birth date and parents' marriage date in individuals and return error List"""
    for fam in ged_data["FAM"]:
        # print(people.get_string(fields=["Name"]))
        if fam["FAM_CHILD"][0] != 'NA':
            # find children
            chId = fam["FAM_CHILD"][0]
            # print(chId)
            for children in ged_data["INDI"]:
                # if children['INDI'] == "@" + chId + "@":
                # print(children["BIRT"])
                # print(fam["MARR"])
                # compare children's birth date and parents's marriage date
                if "Birthday" in ged_data["INDI"] and "Married" in ged_data["FAM"]:
                    bir_date = children["BIRT"]
                    mar_date = fam["MARR"]
                    bir_date = datetime.datetime.strptime(bir_date, '%Y-%m-%d')
                    mar_date = datetime.datetime.strptime(mar_date, '%Y-%m-%d')
                    if (bir_date - mar_date).days < -9:
                        return True
                    else:
                        return False


# US12: Parents not too old
# Mother should be less than 60 years older than her children 
# and father should be less than 80 years older than his children
# Hengyuan Zhang
def parents_not_old():
    for family in family_dic.values():
        husband_flag = False
        wife_flag = False

        if "husband_object" in family and family["husband_object"] != 'NA':
            husband_age = family["husband_object"]["AGE"]
            husband_flag = True

        if "wife_object" in family and family["wife_object"] != 'NA':
            wife_age = family["wife_object"]["AGE"]
            wife_flag = True

        if "children_objects" in family and family["children_objects"] != 'NA':
            for child in family["children_objects"]:
                child_age = child["AGE"]
                husband_to_child = int(husband_age) - int(child_age)
                wife_to_child = int(wife_age) - int(child_age)

                if husband_flag and husband_to_child >= 80:
                    error_array.append(
                        f'ERROR: INDIVIDUAL: US12: {family["husband_object"]["INDI_LINE"]}: {family["FAM"]}: Father is {husband_to_child} older than the child {child["INDI"]}.')

                if wife_flag and wife_to_child >= 60:
                    error_array.append(
                        f'ERROR: FAMILY: US12: {family["wife_object"]["AGE"]}: {family["FAM"]}: Wife is {wife_to_child} older than the child {child["INDI"]}.')


# US13: Siblings spacing
# Birth dates of siblings should be more than 8 months apart or less than 2 days apart 
# (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)
# Hengyuan Zhang
def siblings_spacing():
    list_error = []
    create_family_dic()
    for family_id in family_dic:
        family = family_dic[family_id]
        # more than 1 child
        if len(family["FAM_CHILD"]) > 1:
            list_birth = []
            for child in family["FAM_CHILD"]:
                for indivisual_id in individuals:
                    indi = individuals[indivisual_id]
                    if child == indi:
                        bir_date_str = indi["BIRT"]
                        bir_date = datetime.datetime.strptime(bir_date_str, '%Y-%m-%d')
                    list_birth.append(bir_date)
            list_birth.sort()
            for i in range(1, len(list_birth) - 1):
                if ((list_birth[i] - list_birth[i - 1]).months < 8 and (list_birth[i] - list_birth[i - 1]).days > 2):
                    log = family + "has a wrong date: Birth dates of siblings should be more than 8 months apart or less than 2 days apart."
                    list_error.append(log)
    return list_error


# US42: Reject illegitimate dates
# All dates should be legitimate dates for the months specified
# Muyang Li
def rejectIllegitimateDates():
    list_error = []
    for indivisual_id in individuals:
        indi = individuals[indivisual_id]
        if "BIRT" in indi and "DEAT" in indi:
            bir_date = indi["BIRT"]
            death_date = indi["DEAT"]
            bir_date = datetime.datetime.strptime(bir_date, '%Y-%m-%d')
            death_date = datetime.datetime.strptime(death_date, '%Y-%m-%d')
            if indi["BIRT"] | indi["DEAT"] is None:
                log = indi + "has a wrong date: Date is not illegitimate date."
                list_error.append(log)
            else:
                log = indi + "has legitimate dates."
                list_error.append(log)
            return list_error

        if "MARR" in indi and "DIV" in indi:
            mar_date = indi["MARR"]
            div_date = indi["DIV"]
            mar_date = datetime.datetime.strptime(mar_date, '%Y-%m-%d')
            div_date = datetime.datetime.strptime(div_date, '%Y-%m-%d')
            if indi["MARR"] | indi["DIV"] is None:
                log = indi + "has a wrong date: Date is not illegitimate date."
                list_error.append(log)
            else:
                log = indi + "has legitimate dates."
                list_error.append(log)
            return list_error


# US22: All individual IDs should be unique
# and all family IDs should be unique
# Yikan Wang Sprint2
def unique_ID():
    result = set()
    filter = set()
    for fam in ged_data["FAM"]:
        if fam['FAM'] in filter:
            result.add(fam['FAM'])
        filter.add(fam['FAM'])

    for indi in ged_data["INDI"]:
        if indi['INDI'] in filter:
            result.add(indi['INDI'])
        filter.add(indi['INDI'])
    anomaly_array.append(f"ANOMALY: repetitve IDs{result}")


# US 23 Yikan Sprint2
# No more than one individual with the
# same name and birth date should appear
# in a GEDCOM file
def unique_birthday():
    result = set()
    filter = set()
    for indi in ged_data["INDI"]:
        if (indi['INDI'], indi['BIRT']) in filter:
            result.add((indi['INDI'], indi['BIRT']))
        filter.add((indi['INDI'], indi['BIRT']))
    anomaly_array.append(f'repetitve name&birthdays{result}')


# USID: 15
# This function checks sibling count
# lingwen Kong
def check_sibling_count():
    for family_id in family_dic:
        family = family_dic[family_id]
        if (len(family["FAM_CHILD"]) > 15):
            anomaly_array.append("ANOMALY: FAMILY: US16: {}: Family has {} siblings which is more than 15 siblings")


# User_Story_30: List all living married people in a GEDCOM file
# Prints out a table with all the living married people's information
# lingwen Kong
def listLivingMarried():
    global individuals
    current_dic = {}
    print("User_Story_30: List all living married people in a GEDCOM file")
    for value in individuals.values():
        print(value)
        if value["ALIVE"] and value["SPOUSE"] != "NA":
            current_dic[value["INDI"]] = value
        elif not value["ALIVE"] and value["SPOUSE"] != "NA":
            anomaly_array.append(
                "ERROR: INDIVIDUAL: US30: {}: Deceased Person is married to Person {}".format(value["INDI"],
                                                                                              "".join(value["SPOUSE"])))
            print("ERROR: INDIVIDUAL: US30: {}: Deceased Person is married to Person {}".format(value["INDI"], "".join(
                value["SPOUSE"])))
    # Use pretty table module to print out the results
    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Spouse"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT", "SPOUSE"]
    return ["US30: Living & Married People Table", allFields, tagNames, current_dic]


# US31: List living single
# List all living people over 30 who have never been married in a GEDCOM file
# Hengyuan Zhang
def list_nomarried_living():
    result = list()
    for indivisual_id in individuals:
        indi = individuals[indivisual_id]
        if "BIRT" in indi:
            birthstr = indi["BIRT"]
            current_date = datetime.datetime.now()
            birthdate = datetime.datetime.strptime(birthstr, '%Y-%m-%d')
            if (current_date - birthdate).years >= 30:
                if "MARR" not in indi:
                    result.insert(indi)
    return result


def get_all_children(individual_object):
    spouses = individual_object["SPOUSE"]
    children = []
    if spouses != 'NA':
        for spouse_family_id in spouses:
            individual_family = family_dic["@" + spouse_family_id + "@"]
            if (len(individual_family["FAM_CHILD"]) > 0) and individual_family["FAM_CHILD"] != "NA":
                children.extend(individual_family["FAM_CHILD"])

    return children


def get_individual_siblings(_id, include_husb, include_wife):
    individual = individuals[_id]
    siblings = []

    if "INDI_CHILD" in individual and individual["INDI_CHILD"] != "NA":
        for family_id in individual["INDI_CHILD"]:
            if family_id == "NA":
                continue
            family = family_dic["@" + family_id + "@"]
            if "FAM_CHILD" in family and family["FAM_CHILD"] != "NA":
                siblings.extend(family["FAM_CHILD"])

            if include_husb:
                if "husband_object" in family and family["husband_object"] != "NA":
                    siblings.extend(get_all_children(family["husband_object"]))

            if include_wife:
                if "wife_object" in family and family["wife_object"] != "NA":
                    siblings.extend(get_all_children(family["wife_object"]))

    siblings = list(set(siblings))

    return siblings


# US18: Siblings should not marry
# Siblings should not marry one another
# Muyang Li
def siblingsnotmarry():
    """ Siblings should not marry one another """
    for individual_id in individuals:
        individual = individuals[individual_id]
        if "SPOUSE" in individual and individual["SPOUSE"] != "NA":
            siblings = get_individual_siblings(individual_id, True, True)
            for spouse_family_id in individual["SPOUSE"]:
                if spouse_family_id == "NA":
                    break
                spouse_family = family_dic["@" + spouse_family_id + "@"]
                spouse_id = None
                if "WIFE" in spouse_family and spouse_family["WIFE"] != "NA":
                    if spouse_family["WIFE"] != individual_id:
                        spouse_id = spouse_family["WIFE"]
                if "HUSB" in spouse_family and spouse_family["HUSB"] != "NA":
                    if spouse_family["HUSB"] != individual_id:
                        spouse_id = spouse_family["HUSB"]
                if spouse_id is not None and spouse_id in siblings:
                    anomaly_array.append("ANOMALY: INDIVIDUAL: US18: {}: {}: Individual married to sibling {}".format(
                        individual["INDI_LINE"], individual_id, spouse_id))


# US33: List orphans
# List all orphaned children (both parents dead and child < 18 years old) in a GEDCOM file
# Muyang Li
def getPeopleById(PersonId):
    results_for_people = ged_data["INDI"]
    for person in results_for_people:
        if person['INDI'] == PersonId:
            return person


def listOrphans():
    """ US33- List of Orphan Children') """
    print('\t' + 'FAMILY ID' + '\t' + 'INDIVIDUAL ID' + '\t\t' + 'NAME')
    results_for_family = ged_data["FAM"]
    for family in results_for_family:
        if 'CHIL' not in family:
            continue
        husband = getPeopleById(family['HUSB'])
        wife = getPeopleById(family['WIFE'])
        if 'DEAT' in husband and 'DEAT  ' in wife:
            for child in family['CHIL']:
                child_name = getPeopleById(child)
                print('\t' + family['FAMID'] + '\t\t' + child + '\t\t\t'
                      + child_name["NAME"][0] + " " + (child_name["NAME"][1]).strip("/"))


# US35: List recent births
# List all people in a GEDCOM file who were born in the last 30 days
# Muyang Li
def list_recent_births():
    global individuals
    print(individuals)
    current_dic = {}
    print("User_Story_30:List all people in a GEDCOM file who were born in the last 30 days")
    for people in individuals:
        if "birthday" in individuals and individuals["birthday"] is not None:
            birth_date = datetime.strptime(individuals["birthday"], "%Y-%m-%d %H:%M:%S")
            delta = datetime.date(datetime.now()) - datetime.date(birth_date)
            if (delta.days < 30 and delta.days >= 0):
                print('\t' + individuals["ID"] + '\t\t\t%-10s' % individuals["NAME"][0] + " %-10s" % (
                    individuals["NAME"][1]).strip(
                    "/") + '\t\t' + individuals['birthday'] + '\t\t' + str(delta.days))


# US34 List large age difference
# this function list out large age difference between spouse
# lingwen Kong
def large_age_diff():
    for value in family_dic.values():
        # for family_id in family_dic:
        family = value["FAM"]
        if "husband_object" in family_dic[family]:
            husband = family_dic[family]["husband_object"]
            hage = int(husband["AGE"])
        if "wife_object" in family_dic[family]:
            wife = family_dic[family]["wife_object"]
            wage = int(wife["AGE"])
            agediff = hage / wage
            if agediff >= 2 or agediff <= 0.5:
                anomaly_array.append(
                    "ANOMALY: FAMILY: US34: {}: Family with unique id: {} has a large spouse age difference".format(
                        value["FAM_LINE"], value["FAM"]))
    return anomaly_array


# US04 - marriage before divorce
# checking marriage after divorce
# lingwen kong
def is_marriage_before_divorce():
    # Iterating through all individuals
    for currentIndividual in individuals.values():
        # Ignoring all individuals who weren't ever married
        if currentIndividual['SPOUSE'] != 'NA':
            # Iterating through all the families they were related to
            for currentFamily in currentIndividual['SPOUSE']:
                for checkingFamily in family_dic.values():
                    if checkingFamily['FAM'] == currentFamily:
                        # Ignoring all the marriages without a divorce
                        if checkingFamily['DIV'] != 'NA':
                            # Checking if a divorce date is before a marriage date
                            if checkingFamily['MARR'] > checkingFamily['DIV']:
                                anomaly_array.append(
                                    "ANOMALY: INDIVIDUAL: US04: {}: {}: Marriage Before Divorce - Marriage Date {} - "
                                    "Divorce Date {}".format(
                                        checkingFamily["MARR_LINE"], currentIndividual['INDI'], checkingFamily['MARR'],
                                        checkingFamily['DIV']))
    return anomaly_array


"""
    Below are the sprint3 of Yikan Wang
"""


# US36: List recent Death
# List all people in a GEDCOM file who died in the last 30 days
# Yikan Wang
def list_recent_deaths():
    print("start")
    print(ged_data["INDI"])
    current_dic = {}
    print("end")
    print("User_Story_35:List all people in a GEDCOM file who were born in the last 30 days")
    for people in ged_data["INDI"]:
        if "DEAT" in people and people["DEAT"] != 'NA':
            death_date = datetime.strptime(people["DEAT"], "%Y - %m - %d")
            delta = datetime.date(datetime.now()) - datetime.date(death_date)
            if (delta.days < 30 and delta.days >= 0):
                print(f'{people["NAME"]} died in the past 30 days')


# US 37 Listrecentsurvivors
# List all living spouses and descendants of people
# in a GEDCOM file who died in the last 30days
def list_recent_survivors():
    died = set()
    survivor = set()
    print("User_Story_35:List all people in a GEDCOM file who were born in the last 30 days")
    for people in ged_data["INDI"]:
        if "DEAT" in people and people["DEAT"] != 'NA':
            death_date = datetime.strptime(people["DEAT"], "%Y - %m - %d")
            delta = datetime.date(datetime.now()) - datetime.date(death_date)
            if (delta.days < 30 and delta.days >= 0):
                print(f'{people["NAME"]} died in the past 30 days')
                died.add(people["INDI"])
                print(died)

    for fam in ged_data["FAM"]:
        print(fam)
        if fam["HUSB"] in died or fam["WIFE"] in died or fam["CHIL"] in died:
            print(f'famlity{fam["FAM"]}')
            survivor.add(fam['HUSB'])
            survivor.add(fam['WIFE'])
            survivor.add(fam['CHIL'])

        survivor = survivor - died
    print(f'survivors{survivor}')


# US38: List upcoming birthdays
# List all living people in a GEDCOM file whose birthdays occur in the next 30 days
# Hengyuan Zhang
def list_living_perple_30():
    result = list()
    dayNow = datetime.datetime.now()
    dayAfter30 = dayNow + datetime.timedelta(days=30)
    for indivisual_id in individuals:
        indi = individuals[indivisual_id]
        if "BIRT" in indi:
            birthstr = indi["BIRT"]
        birthdate = datetime.datetime.strptime(birthstr, '%Y-%m-%d')
        if birthdate >= dayNow and birthdate <= dayAfter30:
            result.insert(indi)
    return result


# US41: Include partial dates
# Accept and use dates without days or without days and months
# Muyang Li
def accpet_partial_dates():
    """ US41-Include Partial Dates """
    return_flag = False
    results_for_family = ged_data["FAM"]
    results_for_people = ged_data["INDI"]

    for res in results_for_people:
        if "BIRT" in res and res["BIRT"] == None:
            # print(str(res["ID"])+ " Has Partial Date in GEDCOM File..")
            message = "Error!!! ..." + str(res["ID"]) + " Has Partial Birthdate in GEDCOM File."
            print('\t' + message)

    for res in results_for_people:
        if "DEAT" in res and res["DEAT"] == None:
            message = "Error!!! ..." + str(res["ID"]) + " Has Partial Deathdate in GEDCOM File."
            print('\t' + message)

    for res in results_for_family:
        if "MARR" in res and res["MARR"] == None:
            message = "Error!!! ..." + str(res["FAMID"]) + " Has Partial Marriage Date in GEDCOM File."
            print('\t' + message)

    for res in results_for_family:
        if "DIV" in res and res["DIV"] == None:
            message = "Error!!! ..." + str(res["ID"]) + " Has Partial Divorce Date in GEDCOM File."
            print('\t' + message)


# US42
# Lingwen Kong
# validate dates
def validate_date():
    for value in individuals.values():
        if (value["BIRT"] != "NA"):
            birth = value["BIRT"]
            try:
                datetime.strptime(birth, '%Y-%m-%d')
            except ValueError:
                error_array.append(
                    "ERROR: INDIVIDUAL: US42:  Individual {} does not have valid Birth Date {}".format(
                        value["INDI"], value["BIRT"]))

        if (value["DEAT"] != "NA"):
            death = value["DEAT"]
            try:
                datetime.strptime(death, '%Y-%m-%d')
            except ValueError:
                error_array.append(
                    "ERROR: INDIVIDUAL: US42: Individual {} does not have valid Death Date {}".format(
                        value["INDI"], value["DEAT"]))

    for value in family_dic.values():
        if (value["MARR"] != "NA"):
            marr = value["MARR"]
            try:
                datetime.strptime(marr, '%Y-%m-%d')
            except ValueError:
                error_array.append(
                    "ERROR: FAMILY: US42: Famliy {} does not have valid Marriage Date {}".format(value["FAM"],
                                                                                                       value["MARR"]))

        if (value["DIV"] != "NA"):
            div = value["DIV"]
            try:
                datetime.strptime(div, '%Y-%m-%d')
            except TypeError:

                error_array.append(
                    "ERROR: FAMILY: US42: Famliy {} does not have valid Divorce Date {}".format(value["FAM"],value["DIV"]))
            except ValueError:
                error_array.append(
                    "ERROR: FAMILY: US42: Famliy {} does not have valid Divorce Date {}".format(value["FAM"],
                                                                                                value["DIV"]))
    return error_array


# US39
# lingwen Kong
def list_upcoming_anni():
    """ US39: List all living couples in a GEDCOM file whose marriage anniversaries occur in the next 30 days """

    today_month = int(datetime.today().strftime("%m"))
    today_date = int(datetime.today().strftime("%d"))
    current_dic = {}
    marr_count = 0
    result = True

    for value in family_dic.values():
        if (value["MARR"] == 'NA'):
            error_array.append(
                f'ERROR: FAMILY: US39: {value["FAM_LINE"]}: Family {value["FAM"]} does not have married date!')
            result = False
        else:
            current_marr = value["MARR"]
            current_month = int(current_marr.split("-")[1])
            current_date = int(current_marr.split("-")[2])
            day_difference = (current_month - today_month) * 30 + (current_date - today_date)

            if (day_difference > 0 and day_difference <= 30):
                current_dic[value["FAM"]] = value
                marr_count += 1

    if marr_count > 0:
        allFields = ["ID", "Married", "Husband ID", "Husband Name", "Wife ID", "Wife Name"]
        tagNames = ["FAM", "MARR", "HUSB", "HUSB_NAME", "WIFE", "WIFE_NAME"]
        print_table("US39: List Upcoming Anniversaries Table", allFields, tagNames, current_dic)
    return result


def determine_days(date1, date2):
    year1 = int(date1.split('-')[0])
    month1 = int(date1.split('-')[1])
    day1 = int(date1.split('-')[2])

    if date2 == None:
        year2 = int(datetime.today().strftime("%Y"))
        month2 = int(datetime.today().strftime("%m"))
        day2 = int(datetime.today().strftime("%d"))
    else:
        year2 = int(date2.split('-')[0])
        month2 = int(date2.split('-')[1])
        day2 = int(date2.split('-')[2])

    return (year2 - year1) * 365 + (month2 - month1) * 30 + day2 - day1


# US09
# lingwen Kong
def birth_before_death_parents():
    """ US09: Birth before death of parents """
    global error_array
    error_array = []
    for family in family_dic.values():
        if "children_objects" in family:
            if "husband_object" in family:
                husband_death = family["husband_object"]["DEAT"]
            if "wife_object" in family:
                wife_death = family["wife_object"]["DEAT"]
            for child in family["children_objects"]:
                if (wife_death != "NA"):
                    if (determine_days(child["BIRT"], wife_death) < 0):
                        error_array.append(
                            f"ERROR: INDIVIDUAL: US09: {child['INDI']}: Child was born at {child['BIRT']} after death of mother {wife_death}")
                if (husband_death != "NA"):
                    if (determine_days(husband_death, child["BIRT"]) / 30 > 9):
                        error_array.append(
                            f"ERROR: INDIVIDUAL: US09: {child['INDI']}: Child was born at {child['BIRT']} after 9 month death of father {husband_death}")


def is_spouse_a_child(individual_id, spouse_id):
    individual_object = individuals[individual_id]
    if 'SPOUSE' in individual_object and individual_object['SPOUSE'] != 'NA':
        for spouse_fam in individual_object['SPOUSE']:
            if spouse_fam in family_dic:
                family_temp = family_dic[spouse_fam]
                if "FAM_CHILD" in family_temp and spouse_id in family_temp["FAM_CHILD"]:
                    return True
        return False


# US17
# lingwen kong
def check_parent_child_marriage():
    for family_id in family_dic:
        family_temp = family_dic[family_id]
        if "HUSB" in family_temp and family_temp["HUSB"] != 'NA' and "WIFE" in family_temp and family_temp[
            "WIFE"] != 'NA':
            if is_spouse_a_child(family_temp["HUSB"], family_temp["WIFE"]):
                anomaly_array.append("ANOMALY: INDIVIDUAL: US17: {}: {}: Individual married to child {}" \
                                     .format(family_temp["HUSB_LINE"], family_temp["HUSB"], family_temp["WIFE"]))
            if is_spouse_a_child(family_temp["WIFE"], family_temp["HUSB"]):
                anomaly_array.append("ANOMALY: INDIVIDUAL: US17: {}: {}: Individual married to child {}" \
                                     .format(family_temp["WIFE_LINE"], family_temp["WIFE"], family_temp["HUSB"]))


# US21
# lingwen kong
def correct_gender():
    create_family_dic()
    error_array = []
    for family in family_dic.values():
        if "husband_object" in family:
            husband_sex = family["husband_object"]["SEX"]
            if (husband_sex != "M"):
                error_array.append("ERROR: FAMILY: US21: {}: {}: Is Husband and has Sex as Female".format(
                    family["husband_object"]["SEX_LINE"], family["husband_object"]["INDI"]))
        if "wife_object" in family:
            wife_sex = family["wife_object"]["SEX"]
            if (wife_sex != "F"):
                error_array.append(
                    "ERROR: FAMILY: US21: {}: {}: Is Wife and has Sex as Male".format(family["wife_object"]["SEX_LINE"],
                                                                                      family["wife_object"]["INDI"]))


# US26
# lingwen Kong
def check_corresponding_entries():
    for family_id in family_dic:
        family = family_dic[family_id]
        if "HUSB" in family and family["HUSB"] != "NA":
            husband_object = family["husband_object"]
            if husband_object != "NA" and family_id not in husband_object["SPOUSE"]:
                error_array.append(
                    "ERROR: FAMILY: US26: {}: {}: Husband id does not match with family id in individuals spouse entry".format(
                        family["FAM_LINE"], family["HUSB"]))
        if "WIFE" in family and family["WIFE"] != "NA":
            wife_object = family["wife_object"]
            if wife_object != "NA" and family_id not in wife_object["SPOUSE"]:
                error_array.append(
                    "ERROR: FAMILY: US26: {}: {}: Wife id does not match with family id in individuals spouse entry".format(
                        family["FAM_LINE"], family["WIFE"]))
        if "children_objects" in family and family["children_objects"] != "NA":
            for child_object in family["children_objects"]:
                if child_object != "NA" and family_id not in child_object["INDI_CHILD"]:
                    error_array.append(
                        "ERROR: FAMILY: US26: {}: {}: Child id does not match with family id in individuals spouse entry".format(
                            family["FAM_LINE"], child_object["INDI"]))


# US27

def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    return age


def include_individual_ages():
    global individuals
    tmp = individuals
    for currentIndividual in tmp.values():
        if currentIndividual['DEAT'] == 'NA':
            newArr = currentIndividual['BIRT'].split('-')
            age = calculateAge(date(int(newArr[0]), int(newArr[1]), int(newArr[2])))
            currentIndividual['AGE'] = age
        else:
            deathDate = currentIndividual['DEAT'].split('-')
            birthDate = currentIndividual['BIRT'].split('-')
            biggerNumber = calculateAge(date(int(birthDate[0]), int(birthDate[1]), int(birthDate[2])))
            smallerNumber = calculateAge(date(int(deathDate[0]), int(deathDate[1]), int(deathDate[2])))
            finalAge = biggerNumber - smallerNumber
            currentIndividual['AGE'] = finalAge
    individuals = tmp
    return tmp


# US28 List siblings in families by decreasing age, i.e. oldest siblings first
# lingwen kong
def listSiblingsByAge():
    create_family_dic()
    error_count = 0
    print("US28: List siblings by decreasing age")
    for fam in family_dic.values():
        currentSiblings = fam["FAM_CHILD"]
        sibling_count = 1
        if currentSiblings != "NA":
            current_dic = {}
            for sibling in currentSiblings:
                try:
                    siblingAge = individuals[sibling]["AGE"]
                except:
                    continue
                if (siblingAge == "NA"):  # one of the siblings does not have age
                    error_array.append(
                        ("ERROR: FAMILY: US28: {}: Child {} has no age").format(individuals[sibling]["INDI_LINE"],
                                                                                sibling))
                    sibling_count = 0
                    error_count += 1
                    break;
                if int(siblingAge) in current_dic:
                    sibling_list = current_dic[int(siblingAge)]
                    sibling_list.append(sibling)
                    current_dic[int(siblingAge)] = sibling_list
                else:
                    sibling_list = [sibling]
                    current_dic[int(siblingAge)] = sibling_list
            if (sibling_count == 1):
                temp_dic = sorted(current_dic.keys(), reverse=True)
                resultList = []
        else:  # no children in the family
            anomaly_array.append(
                "ANOMALY: FAMILY: US28: {}: Family {} has no children".format(fam["FAM_LINE"], fam["FAM"]))
            error_count += 1
    print("\n")
    return error_count


# US 32: List multiple births
def multiple_birth_same():
    create_family_dic()
    global anomaly_array
    tmp_anomaly = []
    for value in family_dic.values():
        li = {}
        if "children_objects" in value:
            for child in value["children_objects"]:
                temp = str(child["INDI_CHILD"]) + child["BIRT"]
                if temp in li:
                    tmp_anomaly.append(
                        "ANOMALY: FAMILY: US32: {}: The two or more individuals were born at the same time in a family {}".format(
                            value["FAM_LINE"], value["FAM"]))
                else:
                    li[temp] = child["INDI"]
    anomaly_array = anomaly_array +tmp_anomaly
    return tmp_anomaly


if __name__ == '__main__':
    # read file according to conditions
    """
        To all members: plz delete all test codes like below 
            before pushing to Git, otherwise the program will
            print out undesired result when other members testing 
            their codes. --Yikan Wang
    
    """

    ged_data = read_ged_data("test_data.ged")

    indi_table = PrettyTable()
    indi_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]

    fam_table = PrettyTable()
    fam_table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name",
                             "Children"]

    for individual in ged_data["INDI"]:
        print(f'Individual: {individual}')
        indi_id = individual["INDI"].strip('@')
        indi_table.add_row([indi_id, individual["NAME"], individual["SEX"], individual["BIRT"], individual["AGE"],
                            individual["ALIVE"], individual["DEAT"], (",".join(individual["INDI_CHILD"])),
                            (",".join(individual["SPOUSE"]))])

    for family in ged_data["FAM"]:
        print(f'FAM: {family}')

        fam_id = family["FAM"].strip('@')
        fam_table.add_row([fam_id, family["MARR"], family["DIV"], family["HUSB"].strip('@'), family["HUSB_NAME"],
                           family["WIFE"].strip('@'), family["WIFE_NAME"], ({",".join(family["FAM_CHILD"])})])

    with open("output.txt", "w+") as f:
        f.write(str(indi_table))
        f.write(str(fam_table))