import os
import subprocess


# ftrace parsing
def split_threads(img, filename):
    threads = set()
    # img_filename.txt
    with open(f"/opt/output/tracing/{img}_{filename}.txt","r") as rf:
        # collect thread id (pids)
        for line in rf.readlines():
            if "#" in line:
                continue
            else:
                pid = line.strip().split()[0].replace("<...>-","")
                threads.add(pid)
        
        # split syscall tracing per pid
        for pid in threads:
            trace_readlines = subprocess.check_output(f'grep "{pid}" /opt/output/tracing/{img}_{filename}.txt', shell=True).decode().split("\n")
            print(f"{img}_{filename}-{pid}.txt")
            with open(f"/opt/output/tracing/{img}_{filename}-{pid}.txt","w") as wf:
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

# make directory for parsed data
os.system("mkdir -p /opt/output/tracing/split/")

# nignx/node - single
imgnames = ["redis", "tomcat", "httpd", "mongodb", "mysql", "mariadb"]

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
        split_threads(img, filename)



imgnames = ["gcc", "openjdk", "qalc", "lowriter", "bzip2", "gzip", "ghostscript"]

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