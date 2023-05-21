#!/bin/bash
set -e

DIR=$(pwd)
echo $DIR

CRUD=$1
FILENAME=""

# check number of arguments
if [ $# -ne 1 ] ; then
	echo "Usage: $0 C/R/U/D/INIT"
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
        echo "[MongoDB] Create Testing ..."
        FILENAME="c"
        mongosh 127.0.0.1:30001/test --quiet --eval "db.test.insertMany([{ item: 'pants', won: 5000, tags:['blue', 'white'], size:{h:14, w: 21, uom:'cm'}, 'status':'A'}, { item: 'mat', won: 2000, tags:['blank', 'red'], size:{h:27.9, w: 35.5, uom:'cm'}, 'status':'A'},{ item: 'mousepad', won: 3000, tags:['gel', 'green'], size:{h:19, w: 22.85, uom:'cm'}, 'status':'B'}]);" &
        ;;
    "R")
        echo "[MongoDB] Read Testing ..."
        FILENAME="r"
        mongo 127.0.0.1:30001/test --quiet --eval "db.test.find({});" &
        ;;
    "U")
        echo "[MongoDB] Update Testing ..."
        FILENAME="u"
        mongosh 127.0.0.1:30001/test --quiet --eval "db.test.updateMany({'status':'A'},{\$set: {'size.uom':'in'}});" &
        ;;
    "D")
        echo "[MongoDB] Delete Testing ..."
        FILENAME="d"
        mongosh 127.0.0.1:30001/test --quiet --eval "db.test.deleteMany({});" &
        ;;
esac
wait

# ftrace off
echo 0 > /sys/kernel/debug/tracing/tracing_on
echo "tracing off"

# copy ftrace log
cp /sys/kernel/debug/tracing/trace /opt/output/tracing/
mv /opt/output/tracing/trace /opt/output/tracing/mongodb_${FILENAME}.txt

# clear buffer of ftrace
echo > /sys/kernel/debug/tracing/trace
echo "reset trace log" && sleep 1

# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches
