import json
import csv
import pandas as pd
import subprocess
import matplotlib.pyplot as plt


# read all path
path = subprocess.check_output("find /opt/output/perm/path/*.json", shell=True).decode().strip().split()

# read x86_64.syscall
sysNumNameDict = dict()    # {sys_number(key): sys_name(value)}
sysNameNumDict = dict()    # {sys_name(key): sys_number(value)}
with open("/tmp/x86_64.syscall", "r") as f:
    for line in f.readlines():
        if "__NR_" in line:
            sys_name = line.split(" ")[1].replace("__NR_","")
            sys_number = line.split(" ")[2].strip()
            sysNumNameDict[sys_number] = sys_name
            sysNameNumDict[sys_name] = sys_number

syssetDict = dict()
sysset = set()
for p in path:
    # make key
    syssetDict[p.replace("/opt/output/perm/path/","").replace(".json","")] = set()
    # make path set
    with open(p,"r") as f:
        syspathDict = json.load(f)
    for func, syspaths in syspathDict.items():
        for syspath in syspaths:
            for syscall in syspath:
                syssetDict[p.replace("/opt/output/perm/path/","").replace(".json","")].add(syscall)
                sysset.add(syscall)

# make total syscall set csv
sysNmList = list()
for syscall in sysset:
    if syscall in sysNumNameDict:
        sysNmList.append(sysNumNameDict[syscall])
    elif syscall in sysNumNameDict.values():
        sysNmList.append(syscall)
    else:
        print(f"no {syscall}")

with open("./test/syscall_usage.csv","w") as f:
    csvWriter = csv.writer(f)
    for syscall in sysNmList:
        csvWriter.writerow([syscall, sysNameNumDict[syscall]])


"""
row = syssetDict.keys()
col = syssetDict.keys()

similar = [[0]*len(row) for _ in range(len(col))]


for i, r in enumerate(row):
    for j, c in enumerate(col):
        # calculate similarity
        total = syssetDict[r] | syssetDict[c]
        intersec = syssetDict[r] & syssetDict[c]
        if not len(total) == 0:
            sim = len(intersec) / len(total)
            similar[i][j] = sim

df = pd.DataFrame(similar)
df.to_csv("similarity.csv",header=syssetDict.keys(),index=syssetDict.keys())
"""