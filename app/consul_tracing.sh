#!/bin/bash
set -e

DIR=$(pwd)
echo $DIR

TESTCASE=$1
FILENAME=""

# check number of arguments
if [ $# -ne 1 ] ; then
	echo "Usage: $0 1/2/3"
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
case ${TESTCASE} in
    "1")
        echo "Consul Member Test"
        FILENAME="1"
         docker exec -t consul-container consul members &
        ;;
    "I")
        echo "Insert Test"
        FILENAME="i"
        mysql -h127.0.0.1 -P33306 -uroot -ppassword -Dtest -e"INSERT INTO test (name, phone) VALUES ('Andy', '010-1234-5678');INSERT INTO test (name, phone) VALUES ('Brian', '010-4321-8765');INSERT INTO test (name, phone) VALUES ('Emily', '011-4321-5678');" &
        ;;
    "R")
        echo "Read Test"
        FILENAME="r"
        mysql -h127.0.0.1 -P33306 -uroot -ppassword -Dtest -e"select * from test;" &
        ;;
    "U")
        echo "Update Test"
        FILENAME="u"
        mysql -h127.0.0.1 -P33306 -uroot -ppassword -Dtest -e"UPDATE test SET name='Tom'
WHERE name='Brian';" &
        ;;
    "D")
        echo "Delete Test"
        FILENAME="d"
        mysql -h127.0.0.1 -P33306 -uroot -ppassword -Dtest -e"DROP TABLE test;" &
        ;;
esac

wait

# ftrace off
echo 0 > /sys/kernel/debug/tracing/tracing_on
echo "tracing off"

# copy ftrace log
cp /sys/kernel/debug/tracing/trace /opt/output/tracing/
mv /opt/output/tracing/trace /opt/output/tracing/consul_${FILENAME}.txt

# clear buffer of ftrace
echo > /sys/kernel/debug/tracing/trace
echo "reset trace log" && sleep 1

# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches
