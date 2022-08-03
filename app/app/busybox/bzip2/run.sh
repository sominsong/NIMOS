#!bin/bash

####################### <run.sh> #######################
# 
# This shell script is for extracting the system call sequences
# from bzip2 application with using the BusyBox container images.
# <Operation>
# - First, Compress the test.txt file in .bz2 format
# - Second, Unzip the test.txt.bz2 file
# 
########################################################

set -x

# zip testcase
service strace-docker start
docker run --rm -it -v "$PWD":/home/ -w /home/ myzip sh -c "sleep 2; bzip2 -k test.txt"
service strace-docker stop

# unzip testcase
mv test.txt test.txt.bak
service strace-docker start
docker run --rm -it -v "$PWD":/home/ -w /home/ myzip sh -c "sleep 2; bzip2 -kd test.txt.bz2"
service strace-docker stop

set +x