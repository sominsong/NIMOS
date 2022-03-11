import os
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--target', required=True, help='target ftrace log file')
args = parser.parse_args()  # args.target

# make syscall table
if not os.path.isfile('/tmp/x86_64.syscall'):
    # get x86_64 architecture system call table for system call number
    cmd = "cat /usr/include/x86_64-linux-gnu/asm/unistd_64.h > /tmp/x86_64.syscall"
    os.system(cmd)
syscall_num_tbl = dict()    # syscall_num_tbl['syscall number'] = 'syscall name'

with open('/tmp/x86_64.syscall','r') as f:
    for line in f.readlines():
        if "__NR_" in line:
            sys_num = line.strip('\n').split("__NR_")[1].split()
            syscall_num_tbl[sys_num[1]] = sys_num[0]

# get ftrace log
cmd = "awk '{print $1, $5, $6, $7, $8}'"+ f" ./result/{args.target}.txt"
logs = subprocess.check_output(cmd,shell=True).decode().split('\n')
logs = [l.split(" ") for l in logs]
del logs[-1]

# find function part with using ftrace marker
program_start = 0
function_start = 0
function_end = 0
for i,l in enumerate(logs):
    if "tracing_mark_write:" in l and "start" in l and not "program" in l:
        function_start = i
for i,l in enumerate(logs[function_start:]):
    if "tracing_mark_write:" in l and "end" in l:
        function_end = i + function_start
    if (program_start != 0) and (function_start != 0) and (function_end != 0) :
        break

TESTPID = logs[function_start][0]
TESTCODENAME = logs[function_start][2]

print(f"TESTPID : {TESTPID}")
print(f"TEST CODE NAME : {TESTCODENAME}")

# remove trace marker system call
if function_end != 0:                                   # function_end EXIST   
    function_logs = logs[function_start:function_end]   # remove 'write' system call for tracing marker
    # remove other execution file except TESTPID
    real_i = []
    for i, l in enumerate(function_logs):
        if TESTPID in l[0]:
            real_i.append(i)
    real_function_logs = []
    for i in real_i:
        real_function_logs.append(function_logs[i])
    function_logs = real_function_logs   
    del function_logs[-1]
else:                                                   # function_end NO EXIST
    print("NO funtion_end")
    for i,l in enumerate(logs):
        if TESTPID in l[0]:
            function_end = i
    function_logs = logs[function_start:function_end+1]
print(f"TEST PID : {TESTPID}")
print(f"function_start:  {function_start}, function_end:  {function_end}")


# get system calls
with open(f"./result/{args.target}.txt","w") as wf:
    for f in function_logs:
        if "sys_enter:" in f:
            wf.write(f[3] + "\n")
            print(args.target,":",syscall_num_tbl[f[3]],"(",f[3],")")