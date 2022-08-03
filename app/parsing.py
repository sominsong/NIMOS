# Docker Image 실험해서 tracing한 결과들을 parsing해서 data에 저장
import os
import subprocess

# get current path
cwd = os.getcwd()

def get_save_syscall_sequence(file, app, filename):
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
    with open(f"{cwd}/app/data/parsing/{app}/{filename}.txt","w") as f:
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
    with open(f"{cwd}/app/data/parsing/{app}/{filename}.txt","w") as f:
        for syscall in syscall_seq:
            f.write(f"{syscall}\n")



# get all tracing output
# 1) using ftrace
imgnames = ["mongodb", "mysql", "mariadb", "redis", "httpd", "tomcat", "nginx", "node"]
for img in imgnames:
    cmd = f"find /opt/output/tracing -type f -name '{img}_*.txt'"
    files=subprocess.check_output(cmd, shell=True).decode().split('\n')
    files.pop(-1)

    tmp_files = list()
    for file in files:
        if "/old/" in file:
            continue
        else:
            tmp_files.append(file)
    print(f"{img} output file #: {len(tmp_files)}")

    for file in tmp_files:
        filename = file.replace(f"/opt/output/tracing/{img}_","").replace(".txt","")
        print(filename)

        get_save_syscall_sequence(file, img, filename)


# 2) using strace-container
# imgnames = ["openjdk", "gcc", "bzip2", "gzip", "ghostscript", "lowriter", "qalc"]
imgnames = ["openjdk", "gcc", "lowriter", "qalc"]
for img in imgnames:
    cmd = f"find /opt/output/tracing -type f -name '{img}_*.txt'"
    files=subprocess.check_output(cmd, shell=True).decode().split('\n')
    files.pop(-1)

    tmp_files = list()
    for file in files:
        if "/old/" in file:
            continue
        else:
            tmp_files.append(file)
    print(f"{img} output file #: {len(tmp_files)}")

    for file in tmp_files:
        filename = file.replace(f"/opt/output/tracing/{img}_","").replace(".txt","")
        print(filename)

        get_save_syscall_sequence_strace(file, img, filename)
