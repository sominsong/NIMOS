""" 

parsing.py
====================

Thie module is for parsing the traced results of
Docker images.
The Parsed files save under '/opt/output/parsing' directory.

"""

import os
import subprocess

def get_save_syscall_sequence_ftrace(file, app, filename):
    # get syscall sequence
    syscall_seq = []
    with open(file, "r") as f:
        output = f.readlines()
        for line in output: # parsing header, skip
            if line.startswith("#"):
                continue
            elif not "sys" in line:
                continue
            else:   # parsing start
                if "->" in line:    # sys_exit, skip
                    continue
                else:
                    syscall = line.split("sys_")[1].split("(")[0]
                    syscall_seq.append(syscall)

    # save syscall sequence
    with open(f"/opt/output/parsing/{app}_{filename}.txt","w") as f:
        for syscall in syscall_seq:
            f.write(f"{syscall}\n")

def get_save_syscall_sequence_strace(file, app, filename):
    # syscall_transition
    sys_trans= {"stat": "newstat", "fstat": "newfstat","lstat": "newlstat",
                "uname": "newuname","prlimit": "prlimit64","pread": "pread64",
                "sigreturn": "rt_sigreturn", "pwrite": "pwrite64"}
    # get syscall sequence
    syscall_seq = []
    with open(file, "r") as f:
        output = f.readlines()
        for line in output: # parsing start
            if "procexit" in line or "signaldeliver" in line:    # procexit, skip
                continue
            elif line == "\n":
                continue
            else:
                syscall = line.split()[1]
                if syscall in sys_trans.keys():
                    syscall = sys_trans[syscall]
                syscall_seq.append(syscall)

    # save syscall sequence
    with open(f"/opt/output/parsing/{app}_{filename}.txt","w") as f:
        for syscall in syscall_seq:
            f.write(f"{syscall}\n")

if __name__ == "__main__":
    # make parsing output directory
    if os.path.isdir("/opt/output/parsing/"):
        os.system("rm /opt/output/parsing/*")
    else:
        os.system("mkdir -p /opt/output/parsing/")

    # get all tracing output
    # 1) using ftrace
    imgnames = ["mongodb", "mysql", "mariadb", "redis", "httpd", "tomcat", "nginx", "node"]
    for img in imgnames:
        cmd = f"find /opt/output/tracing/split -type f -name '{img}_*.txt'"
        files=subprocess.check_output(cmd, shell=True).decode().split('\n')
        files.pop(-1)
        print(f"{img} output file #: {len(files)}")

        for file in files:
            filename = file.replace(f"/opt/output/tracing/split/{img}_","").replace(".txt","")
            print(filename)

            get_save_syscall_sequence_ftrace(file, img, filename)


    # 2) using strace-container
    files = []
    imgnames = ["openjdk", "gcc", "bzip2", "gzip", "ghostscript", "lowriter", "qalc"]
    for img in imgnames:
        cmd = f"find /opt/output/tracing/split -type f -name '{img}_*.txt'"
        files=subprocess.check_output(cmd, shell=True).decode().split('\n')
        files.pop(-1)
        print(f"{img} output file #: {len(files)}")

        for file in files:
            filename = file.replace(f"/opt/output/tracing/split/{img}_","").replace(".txt","")
            print(filename)

            get_save_syscall_sequence_strace(file, img, filename)
