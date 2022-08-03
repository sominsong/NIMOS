#!bin/bash

####################### <run.sh> #######################
# 
# This shell script is for extracting the system call sequences
# from gzip application with using the BusyBox container images.
# <Operation>
# - First, Compress the test1.txt and test2.txt files in .gz format
# - Second, Unzip all .gz files
# 
########################################################

set -x

# zip testcase
service strace-docker restart
docker run --rm --name gzip-container  -v "$PWD":/home/ -w /home/ mygzip sh -c "sleep 2; gzip *.txt"

# unzip testcase
service strace-docker restart
docker run --rm --name gzip-container  -v "$PWD":/home/ -w /home/ mygzip sh -c "sleep 2; gzip -d *.gz"

set +x