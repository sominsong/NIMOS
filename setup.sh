#!/bin/bash

OUTPUT_DIR="/opt/output/"

# make output directory
mkdir -pv ${OUTPUT_DIR} ${OUTPUT_DIR}temp/ ${OUTPUT_DIR}perm/
mkdir -pv ${OUTPUT_DIR}perm/path/
mkdir -pv ${OUTPUT_DIR}temp/testcase/
cp -r ./syscall-generation/testcase/* ${OUTPUT_DIR}temp/testcase/
mkdir -pv ${OUTPUT_DIR}temp/testcase/result

# searchsploit
sudo git clone https://github.com/offensive-security/exploitdb.git ${OUTPUT_DIR}perm/exploitdb
sudo ln -sf ${OUTPUT_DIR}perm/exploitdb/searchsploit /usr/local/bin/searchsploit
searchsploit -u

# ftrace setting
echo 1 > /sys/kernel/debug/tracing/events/raw_syscalls/sys_enter/enable
echo 1 > /sys/kernel/debug/tracing/events/raw_syscalls/sys_exit/enable