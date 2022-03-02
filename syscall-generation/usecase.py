""" 

usecase.py
====================

Thie module is for getting use case of API function
used in exploit codes.

Todo:
  * 
"""
import subprocess
import csv
import re

from skip_function_list import skip_list

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tool import Logging
log = Logging.Logging("info")

PERM_OUTPUT_PATH = "/opt/output/perm/"
TEMP_OTUPUT_PATH = "/opt/output/temp/"
EXPLOITDB_PATH = "/exploit/exploit-db/"


def get_original():
    """get original file list in output dictionary

    Returns:
        orgList(list): original file list
    """
    orgList = list()

    find_result = subprocess.check_output(f"find {TEMP_OTUPUT_PATH}*.c.004t.original",shell=True).decode().split("\n")
    find_result.pop(-1)

    for EID in find_result:
        orgList.append(EID)

    return orgList


def get_funUseCase(EID):
    """getting use case of API function used in exploit codes.

    Args:
        eList(list): List of EID

    Returns:
        funcUseCase(dict): dictionary with key(= function name), value(= list of API function use case)
    """
    funcUseCase = dict()
    key = ""
    with open(f"{EID}", "r") as f:
        for line in f.readlines():
            if ";; Function" in line:
                key = line.split()[2]
                funcUseCase[key] = list()
            if re.search("\w \([\w\W\(\)]*\);$", line):
                funcUseCase[key].append(re.findall("\w+ \([\w\W\(\)]*\);$", line.strip())[0])

    for func in skip_list:
        if func in funcUseCase:
            del funcUseCase[func]

    return funcUseCase


def save_funcUseCase(funcUseCase, EID):
    """save use case of API function used in exploit codes into csv file(column: EID, func, API use case).

    Args:
        funcUseCase(dict): dictionary with key(= function name), value(= list of API function use case)
        EID(str): exploit ID
    """
    EID = EID.split("/")[-1].replace(".c.004t.original","")
    with open(f"{PERM_OUTPUT_PATH}usecase.csv", "a", encoding="utf-8") as f:
        wr = csv.writer(f)
        for func, APIList in funcUseCase.items():
            for API in APIList:
                wr.writerow([f"{EID}",f"{func}",f"{API}"])


if __name__ == "__main__":
    orgList = get_original()

    # orgList = ["/opt/output/temp/12.c.004t.original"]

    # Initialization
    with open(f"{PERM_OUTPUT_PATH}usecase.csv","w",encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["EID","func","API use case"])


    for EID in orgList:
        funcUseCase = get_funUseCase(EID)
        save_funcUseCase(funcUseCase, EID)
