""" 

parsingPerThread.py
====================

Thie module is for spliting the traced results of
Docker images per thread.
The splited files save under '/opt/output/tracing/split' directory.

"""

import os
import subprocess


# ftrace parsing
def split_threads_for_ftrace(img, filename):
    threads = set()
    # img_filename.txt
    with open(f"/opt/output/tracing/{img}_{filename}.txt","r") as rf:
        # collect thread id (pids)
        for line in rf.readlines():
            if "#" in line:
                continue
            else:
                # pid = line.strip().split()[0].replace("<...>-","")
                print(line.strip().split("-")[1].split()[0])
                pid = line.strip().split("-")[1].split()[0]
                threads.add(pid)
        
        # split syscall tracing per pid
        for pid in threads:
            trace_readlines = subprocess.check_output(f'grep "{pid}" /opt/output/tracing/{img}_{filename}.txt', shell=True).decode().split("\n")
            print(f"{img}_{filename}-{pid}.txt")
            with open(f"/opt/output/tracing/split/{img}_{filename}-{pid}.txt","w") as wf:
                for line in trace_readlines:              
                    wf.write(line+"\n")

# strace-container parsing
def split_threads_for_strace(img, filename):
    threads = set()
    # img_filename.txt
    with open(f"/opt/output/tracing/{img}_{filename}.txt","r") as rf:
        # collect thread id (pids)
        for line in rf.readlines():
            pid = line.strip().split()[0]
            threads.add(pid)
        
        # split syscall tracing per pid
        for pid in threads:
            trace_readlines = subprocess.check_output(f'grep "{pid}" /opt/output/tracing/{img}_{filename}.txt', shell=True).decode().split("\n")
            print(f"{img}_{filename}-{pid}.txt")
            with open(f"/opt/output/tracing/split/{img}_{filename}-{pid}.txt","w") as wf:
                for line in trace_readlines:
                    wf.write(line+"\n")


if __name__ == "__main__":
    # make directory for parsed data
    if os.path.isdif("/opt/output/tracing/split"):
        os.system("rm /opt/output/tracing/split/*")
    else:
        os.system("mkdir -p /opt/output/tracing/split/")

    # except nignx/node - single
    imgnames = ["redis", "tomcat", "httpd", "mongodb", "mysql", "mariadb"]

    # make parsed files for ftrace output files
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
            split_threads_for_ftrace(img, filename)



    imgnames = ["gcc", "openjdk", "qalc", "lowriter", "bzip2", "gzip", "ghostscript"]

    # make parsed files for strace otuput files
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
            split_threads_for_strace(img, filename)