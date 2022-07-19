
import os
import csv
import json
import pickle
import datetime
import subprocess
from itertools import product
import concurrent.futures

PERM_OUTPUT_PATH = "/opt/output/perm/"
PATH_PATH = "./analysis/new_path/"

MIN_SUPPORT = 2
MAX_N = 200

TEST = False

def check_ngram_for_L1(jsonDict, item):
    existNgram = False
    for funcNm, pathSet in jsonDict.items():
        for path in pathSet:
            if item in path:
                existNgram = True
    return existNgram


def check_ngram(jsonDict, item):
    existNgram = False
    for funcNm, pathSet in jsonDict.items():
        for path in pathSet:
            path = "," + ",".join(path) + ","
            if "," + item + "," in path:
                existNgram = True
    return existNgram


def make_C(pre_L):
    items = set()
    for seqx in pre_L.keys():
        for seqy in pre_L.keys():
            if seqx.split(",")[1:] == seqy.split(",")[:-1]:
                item = seqx + "," + seqy.split(",")[-1]
                items.add(item)
            if seqy.split(",")[1:] == seqx.split(",")[:-1]:
                item = seqy + "," + seqx.split(",")[-1]
                items.add(item)
    return items


def make_L(items, DictList):
    L = dict() # {item[key](str) : support[value](int)}]
    for item in items:
        L[item] = 0
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_ngram = [executor.submit(check_ngram, jsonDict, item) for jsonDict in DictList]
        for future in concurrent.futures.as_completed(future_ngram):
            if future.result():
                L[item] += 1

    # pruning
    for item in items:
        if L[item] < MIN_SUPPORT:
            del L[item]

    return L


def convert_num_name(sysnum):
    if not sysnum.isdigit():
        return sysnum
    cmd = f'grep " {sysnum}$" /tmp/x86_64.syscall'
    sys_name = subprocess.check_output(cmd, shell=True).decode().strip().split()[1].replace("__NR_","")
    return sys_name


pathFile = subprocess.check_output(f"find {PATH_PATH}*.json", shell=True).decode().strip().split()


######
# pathFile = ["/opt/output/perm/path/47163.json", "/opt/output/perm/path/50541.json"]
# TEST = True
######

DictList = list()
for file in pathFile:
    with open(f"{file}", "r") as f:
        DictList.append(json.load(f))

items = set()

# Make C-1
for jsonDict in DictList:
    for funcNm, pathSet in jsonDict.items():
        for path in pathSet:
            for item in path:
                items.add(item)


# Make L-1
L_1 = dict()    # {item[key](str) : support[value](int)}
for item in items:
    L_1[item] = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_ngram_for_L1, jsonDict, item) for jsonDict in DictList]
    
    for future in futures:
        if future.result():
            L_1[item] += 1
    
    
# pruning L-2
for item in items:
    if L_1[item] < MIN_SUPPORT:
        del L_1[item]
    
print(L_1.keys())
    
# Make C-2 (2-items sequences)
items = L_1.keys()
items = list(set(product(items, items)))
items = list(map(lambda x: list(x), items))


# Make L-2
L_2 = dict()
for item in items:
    item = ",".join(item)
    L_2[item] = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_ngram = [executor.submit(check_ngram, jsonDict, item) for jsonDict in DictList] 
    for future in concurrent.futures.as_completed(future_ngram):
        if future.result():
            L_2[item] += 1


# pruning L-2
for item in items:
    item = ",".join(item)
    if L_2[item] < MIN_SUPPORT:
        del L_2[item]

print("L-2: ", L_2.keys())


L = [L_2]
prev_L = L_2

# iterate each process
for i in range(MAX_N-2):
    if not prev_L:
        break
    # Make C-N
    items = set()
    items = make_C(prev_L)
    print(f"\n# of C-{i+3}: ",len(items))
    # Make L-N
    new_L = make_L(items, DictList)
    L.append(new_L.copy())
    print(f"L-{i+3}: ", new_L.keys())
    prev_L = new_L.copy()


month = datetime.datetime.now().month
day = datetime.datetime.now().day

if TEST == False: # 전체 N-gram

    with open(f"{PERM_OUTPUT_PATH}analysis/ngram_result.pkl", "wb") as f:
        pickle.dump(L, f)

    # ngram result with system call number
    with open(f"{PERM_OUTPUT_PATH}analysis/{month}{day}_ngram_sysnum_max{MAX_N}.csv", "w", newline = "", encoding='utf-8') as file:
        f = csv.writer(file)
        f.writerow(["N", "N-gram", "count"])
        for L_x in L:
            for Ngram, cnt in L_x.items():
                f.writerow([len(Ngram.split(',')), cnt, Ngram.split(',')])

    # ngram result with system call name
    sysNameList = list()
    with open(f"{PERM_OUTPUT_PATH}analysis/{month}{day}_ngram_sysname_max{MAX_N}.csv", "w", newline = "", encoding='utf-8') as file:
        f = csv.writer(file)
        f.writerow(["N", "count", "N-gram"])
        for L_x in L:
            for Ngram, cnt in L_x.items():
                sysNameList = list()
                for syscall in Ngram.split(","):
                    sysNameList.append(convert_num_name(syscall))
                f.writerow([len(Ngram.split(',')), cnt, sysNameList])
else:   # TESTN-gram
    # ngram result with system call name
    """
    sysNameList = list()
    with open(f"{month}{day}_ngram_sysname_max{MAX_N}.csv", "w", newline = "", encoding='utf-8') as file:
        f = csv.writer(file)
        f.writerow(["N", "count", "N-gram"])
        for L_x in L:
            for Ngram, cnt in L_x.items():
                sysNameList = list()
                for syscall in Ngram.split(","):
                    sysNameList.append(convert_num_name(syscall))
                f.writerow([len(Ngram.split(',')), cnt, sysNameList])
    """