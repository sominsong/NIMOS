#!/bin/bash
set -e

DIR=$(pwd)
echo $DIR

PORT=8009
REQUEST=$1
CONCUR=$2
FILENAME=$3

# check number of arguments
if [ $# -ne 3 ] ; then
	echo "Usage: $0 requests concurrency ftrace_log_filename"
	exit 0
fi

# clear cache
echo "drop caches..."
echo 3 > /proc/sys/vm/drop_caches

# clear buffer of ftrace
echo > /sys/kernel/debug/tracing/trace
echo "reset trace log" && sleep 1

# ftrace on
echo 1 > /sys/kernel/debug/tracing/tracing_on
echo "tracing on"&& sleep 1

# run test
ab -l -r -n ${REQUEST} -c ${CONCUR} -k -H "Accept-Encoding: gzip,  deflate" http://127.0.0.1:${PORT}/ &
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
