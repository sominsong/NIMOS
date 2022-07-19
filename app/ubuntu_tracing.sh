#!/bin/bash
set -e

DIR=$(pwd)
echo $DIR

CMD=$1
FILENAME=""

# check number of arguments
if [ $# -ne 1 ] ; then
	echo "Usage: $0 CMD"
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
case ${CMD} in
	"ls")
		echo "ls Test"
		FILENAME="ls"
		docker exec ubuntu-container bash -c "ls" &
        ;;
    "whoami")
        echo "whoami Test"
		FILENAME="whoami"
		docker exec ubuntu-container bash -c "whoami" &
        ;;
    "whoami")
        echo "whoami Test"
		FILENAME="whoami"
		docker exec ubuntu-container bash -c "whoami" &
        ;;
    *)
        echo "Invalid argument"
        exit 1
        ;;
esac
wait

# ftrace off
echo 0 > /sys/kernel/debug/tracing/tracing_on
echo "tracing off"

# copy ftrace log
cp /sys/kernel/debug/tracing/trace /opt/output/tracing/
mv /opt/output/tracing/trace /opt/output/tracing/ubuntu_${FILENAME}.txt

# clear buffer of ftrace
echo > /sys/kernel/debug/tracing/trace
echo "reset trace log" && sleep 1
