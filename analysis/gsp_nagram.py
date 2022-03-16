# https://analytics4everything.tistory.com/105

import os
import csv
import json
import subprocess
from itertools import product
import concurrent.futures

PERM_OUTPUT_PATH = "/opt/output/perm/"

MIN_SUPPORT = 2


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
            if seqx.split(",")[-1] == seqy.split(",")[0]:
                item = seqx + "," + seqy.split(",")[-1]
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


pathFile = subprocess.check_output(f"find {PERM_OUTPUT_PATH}path/*.json", shell=True).decode().strip().split()

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


# Make C-3
items = set()
items = make_C(L_2)
print("\n# of C-3: ",len(items))
# Make L-3
L_3 = make_L(items, DictList)
print("L-3: ", L_3.keys())


# Make C-4
items = set()
items = make_C(L_3)
print("\n# of C-4: ",len(items))
# Make L-4
L_4 = make_L(items, DictList)
print("L-4: ",L_4.keys())

# Make C-5
items = set()
items = make_C(L_4)
print("\n# of C-5: ",len(items))
# Make L-5
L_5 = make_L(items, DictList)
print("L-5: ",L_5.keys())

# Make C-6
items = set()
items = make_C(L_5)
print("\n# of C-6: ",len(items))
# Make L-5
L_6 = make_L(items, DictList)
print("L-6: ",L_5.keys())

L = [L_2, L_3, L_4, L_5, L_6]

with open(f"./ngram.csv", "w", newline = "") as file:
    f = csv.writer(file)
    f.writerow(["N", "N-gram", "count"])
    for L_x in L:
        for Ngram, cnt in L_x.items():
            f.writerow([len(Ngram.split(',')), Ngram, cnt])