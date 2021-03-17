from datetime import datetime
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
def list_deceased() -> object:
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
def is_age_legal() -> List:
    """ Less then 150 years old
    :rtype: object
    """
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


if __name__ == '__main__':
    # read file according to conditions
    ged_data = read_ged_data("test_data.ged")

    for family in ged_data["FAM"]:
        husband = family["HUSB"] if "HUSB" in family else []

    indi_table = PrettyTable()
    indi_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    fam_table = PrettyTable()
    fam_table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name",
                             "Children"]

    for individual in ged_data["INDI"]:
        indi_id = individual["INDI"].strip('@')
        indi_table.add_row([indi_id, individual["NAME"], individual["SEX"], individual["BIRT"], individual["AGE"],
                            individual["ALIVE"], individual["DEAT"], (",".join(individual["INDI_CHILD"])),
                            (",".join(individual["SPOUSE"]))])

    for family in ged_data["FAM"]:
        fam_id = family["FAM"].strip('@')
        fam_table.add_row([fam_id, family["MARR"], family["DIV"], family["HUSB"].strip('@'), family["HUSB_NAME"],
                           family["WIFE"].strip('@'), family["WIFE_NAME"], ({",".join(family["FAM_CHILD"])})])

    # print tables
    print(indi_table)
    print(fam_table)

    # output to file
    with open("output.txt", "w+") as f:
        f.write(str(indi_table))
        f.write(str(fam_table))

