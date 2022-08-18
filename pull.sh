#!/bin/bash

# Let's pull Sominsong97 registry images
docker_images=("qalc" "ghostscript" "lowriter" "bzip2" "gcc" "gzip" "openjdk" "myhttpd" "mytomcat" "newnode" "mynginx" "mariadb1" "mariadb2" "redis1" "redis2" "redis3" "mysql" "mongo1" "mongo2" "mongo3")
for img in ${docker_images[@]}
do
    docker pull sominsong97/hyper-seccomp:${img}
done