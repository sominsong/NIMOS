#!/bin/bash
set -e

DIR=$(pwd)
echo $DIR

CRUD=$1
FILENAME=""

# check number of arguments
if [ $# -ne 1 ] ; then
	echo "Usage: $0 C/R/U/D"
	exit 0
fi

# clear buffer of ftrace
echo > /sys/kernel/debug/tracing/trace
echo "reset trace log" && sleep 1

# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches

# ftrace on
echo "tracing on"
echo 1 > /sys/kernel/debug/tracing/tracing_on
sleep 1

# run test
case ${CRUD} in
    "C")
        echo "Create Test"
        FILENAME="c"
        redis-cli -h localhost -p 6379 hmset username:tom phone 010-1234-5678 &
        ;;
    "R")
        echo "Read Test"
        FILENAME="r"
        redis-cli -h localhost -p 6379 hmget username:tom phone &
        ;;
    "U")
        echo "Update Test"
        FILENAME="u"
        redis-cli -h localhost -p 6379 rename username:tom username:amiley &
        ;;
    "D")
        echo "Delete Test"
        FILENAME="d"
        redis-cli -h localhost -p 6379 flushall &
        ;;
esac

wait

# ftrace off
echo 0 > /sys/kernel/debug/tracing/tracing_on
echo "tracing off"

# copy ftrace log
cp /sys/kernel/debug/tracing/trace /opt/output/tracing/
mv /opt/output/tracing/trace /opt/output/tracing/redis_${FILENAME}.txt

# clear buffer of ftrace
echo > /sys/kernel/debug/tracing/trace
echo "reset trace log" && sleep 1

# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches
