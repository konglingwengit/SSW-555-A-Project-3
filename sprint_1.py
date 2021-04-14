from datetime import datetime, time
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


def create_individuals_map():
    global individuals
    individuals = {}

    for individual in document["INDI"]:
        individuals[individual["INDI"]] = individual


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
                        else:
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
    list_error = []
    for indivisual_id in individuals:
        indi = individuals[indivisual_id]
        if "BIRT" in indi:
            datestr = indi["BIRT"]
        elif "DEAT" in indi:
            datestr = indi["DEAT"]
        elif "DIV" in indi:
            datestr = indi["DIV"]
        elif "MARR" in indi:
            datestr = indi["MARR"]
        else:
            continue
        current_date = datetime.datetime.now()
        date = datetime.datetime.strptime(datestr, '%Y-%m-%d')
        if (current_date - date).days < 0:
            log = indi + "has a inavilable date:" + datestr
            list_error.append(log)
    return list_error


# US02: Birth before marriage
# Birth should occur before marriage of an individual
# Hengyuan Zhang
def bir_bef_mar():
    """ store birth and marriage date in individuals and return error list"""
    list_error = []
    for indivisual_id in individuals:
        indi = individuals[indivisual_id]
        if "BIRT" in indi and "MARR" in indi:
            bir_date_str = indi["BIRT"]
            mar_date_str = indi["MARR"]
            bir_date = datetime.datetime.strptime(bir_date_str, '%Y-%m-%d')
            mar_date = datetime.datetime.strptime(mar_date_str, '%Y-%m-%d')
            if (bir_date - mar_date).days >= 0:
                log = indi + "has a inavilable date: Birth date is after marriage date."
                list_error.append(log)
        else:
            log = indi + "doesn't have marriage date."
            list_error.append(log)
    return list_error


# USO3: Birth before death
# Birth should occur before death of an individual
# Muyang Li
def birth_before_death():
    """ store birth date and death in individuals and return error list"""
    list_error = []
    for indivisual_id in individuals:
        indi = individuals[indivisual_id]
        if "BIRT" in indi and "DEAT" in indi:
            bir_date = indi["BIRT"]
            death_date = indi["DEAT"]
            bir_date = datetime.datetime.strptime(bir_date, '%Y-%m-%d')
            death_date = datetime.datetime.strptime(death_date, '%Y-%m-%d')
            if (bir_date - death_date).days >= 0:
                log = indi + "has a wrong date: death date is before birth date."
                list_error.append(log)
        else:
            log = indi + "doesn't have dead."
            list_error.append(log)
    return list_error


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
    list_error = []
    for indivisual_id in individuals:
        indi = individuals[indivisual_id]
        if "DIV" in indi and "DEAT" in indi:
            div_date = indi["DIV"]
            death_date = indi["DEAT"]
            div_date = datetime.datetime.strptime(div_date, '%Y-%m-%d')
            death_date = datetime.datetime.strptime(death_date, '%Y-%m-%d')
            if (div_date - death_date).days >= 0:
                log = indi + "has a wrong date: divorce date is after death date."
                list_error.append(log)
        else:
            log = indi + "doesn't have dead."
            list_error.append(log)
    return list_error


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
    list_error = []
    for fam in ged_data["FAM"]:
        if fam["CHIL"] != 'NA':
            child = fam["CHIL"]
            husb = fam["HUSB"]
            wife = fam["WIFE"]
            for indivisual_id in individuals:
                indi = individuals[indivisual_id]
                if indi['NAME'] == child:
                    child_birth_str = indi['BRITH']
                if indi['NAME'] == husb:
                    husb_birth_str = indi['BRITH']
                if indi['NAME'] == wife:
                    wife_birth_str = indi['BRITH']
                child_date = datetime.datetime.strptime(child_birth_str, '%Y-%m-%d')
                husb_date = datetime.datetime.strptime(husb_birth_str, '%Y-%m-%d')
                wife_date = datetime.datetime.strptime(wife_birth_str, '%Y-%m-%d')
                if (child_date - wife_date).years >= 60:
                    log = child + "or" + wife + "has a wrong date: Mother should be less than 60 years older than her children."
                    list_error.append(log)
                if (child_date - husb_date).years >= 80:
                    log = child + "or" + husb + "has a wrong date: father should be less than 80 years older than his children."
                    list_error.append(log)
    return list_error


# US13: Siblings spacing
# Birth dates of siblings should be more than 8 months apart or less than 2 days apart 
# (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)
# Hengyuan Zhang
def siblings_spacing():
    list_error = []
    for family_id in family_dic:
        family = family_dic[family_id]
        # more than 1 child
        if (len(family["FAM_CHILD"]) > 1):
            list_birth = []
            for child in family["FAM_CHILD"]:
                for indivisual_id in individuals:
                    indi = individuals[indivisual_id]
                    if child == indi:
                        bir_date_str = indi["BIRT"]
                        bir_date = datetime.datetime.strptime(bir_date_str, '%Y-%m-%d')
                    list_birth.append(bir_date)
            list_birth.sort()
            for i in range(1,len(list_birth) - 1):
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


#
# # US22: All individual IDs should be unique
# # and all family IDs should be unique
# # Yikan Wang Sprint2
# def unique_ID():
#     result = set()
#     filter = set()
#     print('hello')
#     for fam in ged_data["FAM"]:
#         if fam['FAM'] in filter:
#             result.add(fam['FAM'])
#         filter.add(fam['FAM'])
#
#     for indi in ged_data["INDI"]:
#         if indi['INDI'] in filter:
#             result.add(indi['INDI'])
#         filter.add(indi['INDI'])
#     anomaly_array.append(f"ANOMALY: repetitve IDs{result}")
#
#
# # US 23 Yikan Sprint2
# # No more than one individual with the
# # same name and birth date should appear
# # in a GEDCOM file
# def unique_birthday():
#     result = set()
#     filter = set()
#     for indi in ged_data["INDI"]:
#         if (indi['INDI'], indi['BIRT']) in filter:
#             result.add((indi['INDI'], indi['BIRT']))
#         filter.add((indi['INDI'], indi['BIRT']))
#     anomaly_array.append(f'repetitve name&birthdays{result}')


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
    print(individuals)
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


# US18: Siblings should not marry
# Siblings should not marry one another
# Muyang Li
def siblingsnotmarry():
    """ Siblings should not marry one another """
    for fam in ged_data["FAM"]:
        if fam["FAM_CHILD"][0] != 'NA':
            # find children
            chId = fam["FAM_CHILD"][0]
            #print(chId)
        # if family["FAM_CHILD"] in family:
        #     child = res['CHILDREN']
        #     childd = list(x for x in indi if x["ID"] in child)
        #     # print childd
    for sibling in chId:
        sib_fam = next((x for x in family if x["HUSB"] == sibling["FAM_CHILD"]), None)
        #print(sib_fam)
        if sib_fam and sib_fam["WIFE"] in chId:
            anomaly_array.append("ANOMALY: Sibling is married to another sibling")


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
                print('\t' + individuals["ID"] + '\t\t\t%-10s' % individuals["NAME"][0] + " %-10s" % (individuals["NAME"][1]).strip(
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



if __name__ == '__main__':
    # read file according to conditions
    print(listLivingMarried())
    ged_data = read_ged_data("test_data.ged")

    print('ged_data')
    print(ged_data)
    '''
        for family in ged_data["FAM"]:
            #print(f'family: {family}')
            husband = family["HUSB"] if "HUSB" in family else []
            #print(f'husband:{husband}') # does not make any changes
    '''
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
    # unique_birthday()
    # print tables
    # print(indi_table)
    # print(fam_table)
    # print('test results')
    # print(bir_bef_mar)
    # output to file


    with open("output.txt", "w+") as f:
        f.write(str(indi_table))
        f.write(str(fam_table))

    # Below are for tests
    #
    # print(format_date([17, FEB, 2021]))
