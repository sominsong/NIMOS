#!/bin/bash
set -e

DIR=$(pwd)
echo $DIR

RESTAPI=$1
FILENAME=""

# check number of arguments
if [ $# -ne 1 ] ; then
	echo "Usage: $0 METHOD"
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
		ab -l -c 1 -n 1 http://127.0.0.1:8080/sample/ &
		;;
	"POST")
		echo "POST Test"
		FILENAME="post"
		ab -l -p plain.txt -T application/octet-stream -c 1 -n 1 http://127.0.0.1:8080/sample/ &
		;;
	"PUT")
		echo "PUT Test"
		FILENAME="put"
		ab -l -u plain.txt -T application/octet-stream -c 1 -n 1 http://127.0.0.1:8080/sample/ &
		;;
esac
wait

# ftrace off
echo 0 > /sys/kernel/debug/tracing/tracing_on
echo "tracing off"

# copy ftrace log
cp /sys/kernel/debug/tracing/trace /opt/output/tracing/
mv /opt/output/tracing/trace /opt/output/tracing/tomcat_${FILENAME}.txt

# clear buffer of ftrace
echo > /sys/kernel/debug/tracing/trace
echo "reset trace log" && sleep 1
