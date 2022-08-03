#!bin/bash

####################### <run.sh> #######################
# 
# This shell script is for extracting the system call sequences
# from the GCC container images.
# <Operation>
# - Compile main.c file in gcc folder & Make myapp object file
# 
########################################################

set -x

# compile testcase
service strace-docker start
docker run --rm -v "$PWD":/home/ -w /home/ mygcc bash -c "sleep 5; gcc -o myapp main.c;"
service strace-docker stop

set +x