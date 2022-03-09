""" 

testcase.py
====================

Thie module is for making test case file for API function
with use case of API functions used in exploit codes.

Todo:
  * compile testcase code and save result in output directory
"""
import os
import csv
import json
import requests
from bs4 import BeautifulSoup



API_sysseq = dict() # {API usecase: [syscall sequence]}

PERM_OUTPUT_PATH = "/opt/output/perm/"
TEMP_OTUPUT_PATH = "/opt/output/temp/"
EXPLOITDB_PATH = "/exploit/exploit-db/"
TEST_PATH = "/opt/output/temp/testcase/"


def get_usecase():
    usecase = dict() # {EID: {func: [usecase, ... ]}}
    with open(f"{PERM_OUTPUT_PATH}usecase.csv", "r", encoding="utf-8", newline="") as f:
        rdr = csv.reader(f)
        for line in rdr:    # line[0]: EID, line[1]: func, line[2]: API use case
            EID = line[0]
            if not usecase.get(EID):
                usecase[EID] = dict()
            func = line[1]
            if not usecase[EID].get(func):
                usecase[EID][func] = list()
            API = line[2]
            usecase[EID][func].append(API)
    
    return usecase


def get_checker():
    url = "http://upstream.rosalinux.ru/tests/glibc/2.13/view_tests.html"
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")
    resultset = soup.find_all('span', {'class': ['header','int']})

    
    # get libFuncDict info.
    libFuncDict = dict() # key: library(str), value: API(list)
    library = ""
    for tag in resultset:   
        func = tag.get_text()
        if func[-2:] == ".h":
            library = func
            if not libFuncDict.get(func):
                libFuncDict[library] = list()
        else:
            libFuncDict[library].append(func.split()[0])

    checkerTotalAPI = sum(libFuncDict.values(), [])
    checkerTotalAPI = ' '.join(checkerTotalAPI).split()

    return libFuncDict


def get_testcase(libHeader, API):
    url = f"http://upstream.rosalinux.ru/tests/glibc/2.13/groups/{libHeader}/functions/{API}/view.html"
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")
    resultset = soup.find_all('table', {'class': 'code_lines'})
    testcase = list()
    for tag in resultset:
        rs = tag.find_all('td')
        for t in rs:
            testcase.append(t.get_text().replace("\xa0",""))
    
    return testcase


def find_header(libFuncDict, API):
    # which header library ?
    libHeader = None
    checkerTotalAPI = sum(libFuncDict.values(), []) # get all header and API
    if API in checkerTotalAPI:
        for lib, func in libFuncDict.items():
            if API in func:
                libHeader = lib.replace(".h","")
    return libHeader


def insert_mark(API, testcase, EID, funcname, args):
    # mark
    OPEN_MARK = f'tm_fd = open_tm();'
    START_MARK = f'tm_write_start(tm_fd, "{API}-{EID}-{funcname}", "{args}");'
    END_MARK = f'tm_write_end(tm_fd, "{API}-{EID}-{funcname}");'

    # is target function in one line?
    oneline = False
    start, end = 0, 0
    for i, line in enumerate(testcase):
        if API + "(" in line and "//target call" in line:
            oneline = True
            start, end = i, i
    # if API function in one line
    if oneline:
        # print("This is oneline")
        testcase.insert(start, START_MARK)
        testcase.insert(end+2, END_MARK)
        testcase.insert(start, OPEN_MARK)

    # if API function in multi-line
    else:
        # print("This is multi-line")
        for i, line in enumerate(testcase):
            if API + "(" in line:
                start = i
            if "//target call" in line:
                end = i
        testcase.insert(start, START_MARK)
        testcase.insert(end+2, END_MARK)
        testcase.insert(start, OPEN_MARK)

    testcase.insert(0,'#include "tm.h"')
    # print(testcase)

    return testcase


def save_original_testcase(API, testcase):
    if os.path.isfile(f"{TEST_PATH}{API}-default-default.c"):
        return
    else:   # there is no default unit test file
        with open(f"{TEST_PATH}{API}-default-default.c","w+") as f:
            for line in testcase:
                f.write(line+"\n")


def save_custom_testcase(API, testcase, EID, funcname):
    if os.path.isfile(f"{TEST_PATH}{API}-{EID}-{funcname}.c"):
        # if duplication
        for i in range(100):
            if os.path.isfile(f"{TEST_PATH}{API}-{EID}-{funcname}-{i+1}.c"):
                continue
            else:
                with open(f"{TEST_PATH}{API}-{EID}-{funcname}-{i+1}.c", "w+") as f:
                    for line in testcase:
                        f.write(line+"\n")
                return
    else:   # there is no custom testcase file
        with open(f"{TEST_PATH}{API}-{EID}-{funcname}.c","w+") as f:
            for line in testcase:
                f.write(line+"\n")


def insert_argument(API, usecase, testcase):
    # pre-processing
    if not usecase[-1] == ";":
        usecase = usecase + ";"
    if "))" in usecase:
        usecase = usecase.replace("))",")")
    if "0B" in usecase:
        usecase = usecase.replace("0B","NULL")

    # is target function in one line?
    oneline = False
    start, end = 0, 0
    # find start, end
    for i, line in enumerate(testcase):
        if API + "(" in line and "//target call" in line:
            oneline = True
            start, end = i, i
    # if API function in one line
    if oneline:
        testcase[start] = usecase   # replace custom API
    else:     # if API function in multi-line
        # find start, end
        for i, line in enumerate(testcase):
            if API + "(" in line:
                start = i
            if "//target call" in line:
                end = i
        # remove default API
        for i in range(end-start): 
            testcase.pop(start)
        
        testcase[start] = usecase   # replace custom API

    return testcase


def custom_testcase(testcase, API, usecase, EID, funcname):
    args = usecase.replace(f"{API} (", "").replace(");","").replace('"','\\"')

    testcase = insert_mark(API, testcase, EID, funcname, args)
    # save original
    save_original_testcase(API, testcase)
    # argument custom
    testcase = insert_argument(API, usecase, testcase)
    # save custom testcase
    save_custom_testcase(API, testcase, EID, funcname)


def make_testcase(libFuncDict, API, usecase, EID, funcname):
    libHeader = find_header(libFuncDict, API)
    if libHeader:
        testcase = get_testcase(libHeader, API)
        # print(f"{libHeader}.h : {API}")
        custom_testcase(testcase, API, usecase, EID, funcname)
    else:   # there is no API in checker
        print(f"no {API} in checker")


if __name__ == "__main__":
    usecase = get_usecase()
    libFuncDict = get_checker()  
 
    # get EID, function, API usecase
    for EID, funcAPI in usecase.items():
        for func, APIList in funcAPI.items():
            for API in APIList:
                print(EID, func, API)
                make_testcase(libFuncDict, API.split()[0], API, EID, func)  # make testcase for a API function


        
