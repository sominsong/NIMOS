set -x

# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches

# zip testcase
echo "Tracing Start - zip case"
service strace-docker restart
docker run --rm -it -w /home/ mybzip2 sh -c "sleep 2; bzip2 -k test.txt"
service strace-docker stop

# copy ftrace log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

# unzip testcase
echo "Tracing Start - unzip case"
mv ../data/test.txt ../data/test.txt.bak
service strace-docker restart
docker run --rm -it -w /home/ myzip sh -c "sleep 2; bzip2 -kd test.txt.bz2"
service strace-docker stop

# copy ftrace log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

set +x
