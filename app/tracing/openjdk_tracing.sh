set -x

# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

# zip testcase
echo "Tracing Start - compile case"
service strace-docker restart
docker run --rm --name openjdk-container -w /usr/src/myapp/ sominsong97/hyper-seccomp:openjdk sh -c "sleep 2; javac Main.java"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

set +x