# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-* 2> /dev/null


# zip testcase
echo "Tracing Start - zip case"
service strace-docker restart
docker run --rm -it -w /home/ --name bzip2-container sominsong97/hyper-seccomp:bzip2 sh -c "sleep 2; bzip2 -k test.txt"
service strace-docker stop

# copy ftrace log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/bzip2_zip.txt && sleep 2

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-* 2> /dev/null

# unzip testcase
echo "Tracing Start - unzip case"
mv ../data/test.txt ../data/test.txt.bak
service strace-docker restart
docker run --rm -it -w /home/ --name bzip2-container sominsong97/hyper-seccomp:bzip2 sh -c "sleep 2; bzip2 -kd test.txt.bz2"
service strace-docker stop

# copy ftrace log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/bzip2_unzip.txt && sleep 2

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*  2> /dev/null