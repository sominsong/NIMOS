#!/bin/bash

OUTPUT_DIR="/opt/output/"

# make output directory
mkdir -pv ${OUTPUT_DIR} ${OUTPUT_DIR}temp/ ${OUTPUT_DIR}perm/
mkdir -pv ${OUTPUT_DIR}perm/path/
mkdir -pv ${OUTPUT_DIR}perm/analysis/
mkdir -pv ${OUTPUT_DIR}temp/testcase/
cp -r ./syscall_generation/testcase/* ${OUTPUT_DIR}temp/testcase/
mkdir -pv ${OUTPUT_DIR}temp/testcase/result

# searchsploit
git clone https://gitlab.com/exploit-database/exploitdb.git ${OUTPUT_DIR}perm/exploitdb
ln -sf ${OUTPUT_DIR}perm/exploitdb/searchsploit /usr/local/bin/searchsploit
searchsploit -u


# ftrace setting
echo 1 > /sys/kernel/debug/tracing/events/raw_syscalls/sys_enter/enable
echo 1 > /sys/kernel/debug/tracing/events/raw_syscalls/sys_exit/enable

# Let's pull Sominsong97 registry images
bash pull.sh
