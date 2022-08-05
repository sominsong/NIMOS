#!/bin/bash

####################### <run.sh> #######################
# 
# This shell script is for traing with ftrace.
# 
########################################################

set -e

echo > /sys/kernel/debug/tracing/trace
echo "reset trace log"

echo 1 > /sys/kernel/debug/tracing/tracing_on
echo "tracing on"

timeout -s 9 10s ./$1 2> /tmp/error.txt

echo 0 > /sys/kernel/debug/tracing/tracing_on
echo "tracing off"

cp /sys/kernel/debug/tracing/trace /opt/output/temp/testcase/result/
mv /opt/output/temp/testcase/result/trace /opt/output/temp/testcase/result/$1.txt

python3 get_syscall_from_ftrace.py --target=$1