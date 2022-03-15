# https://analytics4everything.tistory.com/105
import csv
import json
from itertools import product


PERM_OUTPUT_PATH = "/opt/output/perm/"
TEST_EID_1 = "40616"
TEST_EID_2 = "40839"

MIN_SUPPORT = 2

def make_C(pre_L):
    items = set()
    for seqx in pre_L.keys():
        for seqy in pre_L.keys():
            if seqx.split(",")[-1] == seqy.split(",")[0]:
                item = seqx + "," + seqy[-1]
                items.add(item)
    return items

def make_L(items, jsonDict1, jsonDict2):
    L = dict() # {item[key](str) : support[value](int)}]
    exitBool = False
    for item in items:
        L[item] = 0
        for funcNm, pathSet in jsonDict1.items():
            for path in pathSet:
                if item in ",".join(path):
                    exitBool = True
        if exitBool == True:
            L[item] += 1
        exitBool = False
        for funcNm, pathSet in jsonDict2.items():
            for path in pathSet:
                if item in ",".join(path):
                    exitBool = True
        if exitBool == True:
            L[item] += 1
    
    # pruning L
    for item in items:
        if L[item] < MIN_SUPPORT:
            del L[item]

    return L


with open(f"{PERM_OUTPUT_PATH}path/{TEST_EID_1}.json","r") as f:
    jsonDict1 = json.load(f)
with open(f"{PERM_OUTPUT_PATH}path/{TEST_EID_2}.json","r") as f:
    jsonDict2 = json.load(f)


items = set()

# L-1 sequence pattern

# Make C-1
for funcNm, pathSet in jsonDict1.items():
    for path in pathSet:
        for item in path:
            items.add(item)
for funcNm, pathSet in jsonDict2.items():
    for path in pathSet:
        for item in path:
            items.add(item)

# Make L-1
L_1 = dict() # {item[key](str) : support[value](int)}
exitBool = False
for item in items:
    L_1[item] = 0
    for funcNm, pathSet in jsonDict1.items():
        for path in pathSet:
            if item in path:
                exitBool = True
    if exitBool == True:
        L_1[item] += 1
    exitBool = False
    for funcNm, pathSet in jsonDict2.items():
        for path in pathSet:
            if item in path:
                exitBool = True
    if exitBool == True:
        L_1[item] += 1 

# pruning L-1
for item in items:
    if L_1[item] < MIN_SUPPORT:
        del L_1[item]
print(L_1.keys())


# Make C-2 (2-items sequences)
items = L_1.keys()
items = list(set(product(items, items)))
items = list(map(lambda x: list(x), items))
print(items)

L_2 = dict() # {item[key](str) : support[value](int)}
exitBool = False

# Make L-2
for item in items:
    item = ",".join(item)
    L_2[item] = 0
    for funcNm, pathSet in jsonDict1.items():
        for path in pathSet:
            if item in ",".join(path):
                exitBool = True
    if exitBool == True:
        L_2[item] += 1
    exitBool = False
    for funcNm, pathSet in jsonDict2.items():   
        for path in pathSet:
            if item in ",".join(path):
                exitBool = True
    if exitBool == True:
        L_2[item] += 1

# pruning L-2
for item in items:
    item = ",".join(item)
    if L_2[item] < MIN_SUPPORT:
        del L_2[item]
print(L_2.keys())


# Make C-3 (3-items sequence)
items = make_C(L_2)

# Make L-3
L_3 = make_L(items, jsonDict1, jsonDict2)
print("L_3 : ", L_3.keys())

# Make C-4 (4-items sequence)
items = make_C(L_3)

# make L-4
L_4 = make_L(items, jsonDict1, jsonDict2)
print("L_4 : ", L_4.keys())

L = [L_2, L_3, L_4]
print(type(L), type(L[0]))

with open(f"./ngram_{TEST_EID_1}_{TEST_EID_2}.csv", "w", newline = "") as file:
    f = csv.writer(file)
    f.writerow(["N", "N-gram", "count"])
    for L_x in L:
        for Ngram, cnt in L_x.items():
            f.writerow([len(Ngram.split(',')), Ngram, cnt])
