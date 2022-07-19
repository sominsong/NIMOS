#!/bin/bash
set -e


# ftrace on
echo "tracing on"
echo 1 > /sys/kernel/debug/tracing/tracing_on
sleep 1

echo "GCC Test"
sleep 100 &
wait

# ftrace off
echo 0 > /sys/kernel/debug/tracing/tracing_on
echo "tracing off"

# copy ftrace log
cp /sys/kernel/debug/tracing/trace /opt/output/tracing/
mv /opt/output/tracing/trace /opt/output/tracing/gcc.txt

# clear buffer of ftrace
echo > /sys/kernel/debug/tracing/trace
echo "reset trace log" && sleep 1

# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches