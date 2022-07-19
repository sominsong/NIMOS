#!/bin/bash
set -e

DIR=$(pwd)
echo $DIR

WORKLOAD_NUM=$1
FILENAME=$2

# clear buffer of ftrace
echo > /sys/kernel/debug/tracing/trace
echo "reset trace log" && sleep 1

# ftrace on
echo "tracing on"
echo 1 > /sys/kernel/debug/tracing/tracing_on
sleep 1

# run test
# ${DIR}/ycsb-0.17.0/bin/ycsb run mongodb -s -P ${DIR}/ycsb-0.17.0/workloads/workload${WORKLOAD_NUM} -p mongodb.url=mongodb://localhost:27017/ycsb?w=0 &
 ${DIR}/ycsb-0.17.0/bin/ycsb run mongodb -s -P ${DIR}/ycsb-0.17.0/workloads/workload${WORKLOAD_NUM} -p mongodb.url=mongodb://localhost:30001/ycsb?w=0 &
wait

# ftrace off
echo 0 > /sys/kernel/debug/tracing/tracing_on
echo "tracing off"

# copy ftrace log
cp /sys/kernel/debug/tracing/trace /opt/output/tracing/
mv /opt/output/tracing/trace /opt/output/tracing/${FILENAME}.txt

# clear buffer of ftrace
echo > /sys/kernel/debug/tracing/trace
echo "reset trace log" && sleep 1
