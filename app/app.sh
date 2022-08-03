#!bin/bash

####################### <app.sh> #######################
# 
# This shell script is for extracting the system call sequences
# from the execution of a normally operating application.
# 
########################################################

# Shut down all running containers
running_containers=$(docker ps  | grep 'Up' |awk '{print $1}')
for i in ${running_containers}; do
    docker rm -f $i
done

# 