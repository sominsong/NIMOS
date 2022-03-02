import subprocess
import csv
 



def get_funcList(result):
    funcList = []

    result = result.split("\n")
    result.pop(-1)

    for line in result:
        if ": <>" in line:
            funcList.append(line.split()[1].replace(":",""))

    funcList = list(set(funcList))
    return funcList


def save_funcList(funcList, ELOC):
    EID = ELOC.replace("../exploit/exploit-db/","").replace(".c","")
    with open(f'/opt/output/perm/func_usage.csv' ,'a', encoding='utf-8', newline='') as f:
        wr = csv.writer(f)
        for f in funcList:
            wr.writerow([EID,f])


cmd = f"find ../exploit/exploit-db/*.c"
try:
    find_result = subprocess.check_output(cmd,shell=True).decode().split("\n")
except Exception as e:
    print(f"Find Error")

find_result.pop(-1)

# init csv
with open(f'/opt/output/perm/func_usage.csv' ,'w', encoding='utf-8', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(["EID","API"])

find_result = ["../exploit/exploit-db/45553.c"]

# get cflow result
for ELOC in find_result:
    cmd = f"cflow --format=posix --omit-arguments {ELOC}"
    try:
        cflow_result = subprocess.check_output(cmd,shell=True).decode()
        print(cflow_result)
    except Exception as e:
        print(f"cflow error - {ELOC}")
        continue
    funcList = get_funcList(cflow_result)
    save_funcList(funcList, ELOC)