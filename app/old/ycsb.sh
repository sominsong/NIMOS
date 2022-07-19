#!/bin/sh

opt=$1
workload=$2
mongo_url=mongodb://127.0.0.1:27017/ycsb

case ${opt} in
	"help")
		echo "$0 load/run/setup workload"
		;;
	"load")
		echo "drop ycsb database"
		docker exec mongodb-container1 mongo ${mongo_url} --eval "db.dropDatabase()"
		echo "load..."
		# ./ycsb-0.17.0/bin/ycsb load mongodb -s -P ./ycsb-0.17.0/workloads/workload${workload} -p mongodb.url=mongodb://localhost:27017/ycsb?w=0
		./ycsb-0.17.0/bin/ycsb load mongodb -s -P ./ycsb-0.17.0/workloads/workload${workload} -p mongodb.url=mongodb://localhost:30001/ycsb?w=0
		echo "delete cache..."
		echo 3 > /proc/sys/vm/drop_caches
		;;
	"run")
		echo "this is run"
		./ycsb-0.17.0/bin/ycsb run mongodb -s -P ./ycsb-0.17.0/workloads/workload${workload} > /opt/output/YCSB/outputRun.txt
		;;
	"setup")
		echo "setting..."
		export M2_HOME=/usr/local/maven
		export PATH=${M2_HOME}/bin:${PATH}
		;;
esac
