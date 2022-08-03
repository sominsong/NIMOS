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

docker build -t myapache .
docker run -d --name apache-container -p 8009:80 myapache



set +x