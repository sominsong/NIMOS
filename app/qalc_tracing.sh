set -x

# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

# cross product (vector) testcase
echo "Tracing Start - cross product case"
service strace-docker restart
docker run --rm --name qalc-container -w /home/ sominsong97/hyper-seccomp:qalc bash -c "sleep 1; qalc 'cross((1; 2; 3); (4; 5; 6))'"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

# hadamard product (matrix) testcase
echo "Tracing Start - hadamard product case"
service strace-docker restart
docker run --rm --name qalc-container -w /home/ sominsong97/hyper-seccomp:qalc sh -c "sleep 1; qalc 'hadamard([[1; 2; 3]; [4; 5; 6]]; [[7; 8; 9]; [10; 11; 12]])'"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

set +x