#!/bin/bash
set -e

DIR=$(pwd)
echo $DIR

PORT=8009
RESTAPI=$1
FILENAME=""

# check number of arguments
if [ $# -ne 1 ] ; then
	echo "Usage: $0 METHOD/INIT ftrace_log_filename"
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
case ${RESTAPI} in
	"GET")
		echo "GET Test"
		FILENAME="get"
		ab -l -k -c 1 -n 1 http://127.0.0.1:8009/ &
		;;
	"POST")
		echo "POST Test"
		FILENAME="post"
		ab -l -k -p ./app/tracing/plain.txt -c 1 -n 1 http://127.0.0.1:8009/ &
		;;
	"PUT")
		echo "PUT Test"
		FILENAME="put"
		ab -l -k -u ./app/tracing/plain.txt -c 1 -n 1 http://127.0.0.1:8009/ &
		;;
esac
wait

# ftrace off
echo 0 > /sys/kernel/debug/tracing/tracing_on
echo "tracing off"

# copy ftrace log
cp /sys/kernel/debug/tracing/trace /opt/output/tracing/
mv /opt/output/tracing/trace /opt/output/tracing/httpd_${FILENAME}.txt

# clear buffer of ftrace
echo > /sys/kernel/debug/tracing/trace
echo "reset trace log" && sleep 1

# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches
