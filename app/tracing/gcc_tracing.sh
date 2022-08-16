set -x

# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

# compile testcase
echo "Tracing Start - compile case"
service strace-docker restart
docker run --rm -w /home/ sominsong97/hyper-seccomp:gcc bash -c "sleep 5; gcc -o myapp main.c;"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/$2_compile.txt && sleep 2

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

set +x
