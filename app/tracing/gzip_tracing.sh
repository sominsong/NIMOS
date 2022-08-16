set -x

# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

# zip testcase
echo "Tracing Start - zip case"
service strace-docker restart
docker run --rm --name gzip-container -w /home/ sominsong97/hyper-seccomp:gzip sh -c "sleep 2; gzip *.txt"
service strace-docker stop

# # copy tracing log
# echo "Copy tracing results"
# cp /var/log/strace-docker/*-*-* /opt/output/tracing/$2_zip.txt && sleep 2

# # delete cache
# echo "delete cache and lagacy datas"
# echo 3 > /proc/sys/vm/drop_caches
# rm /var/log/strace-docker/*-*-*

# # unzip testcase
# echo "Tracing Start - unzip case"
# docker run --rm --name gzip-container -w /home/ sominsong97/hyper-seccomp:gzip sh -c "mv test*.txt test*.txt.bak"
# service strace-docker restart
# docker run --rm --name gzip-container -w /home/ sominsong97/hyper-seccomp:gzip sh -c "sleep 2; gzip -d *.gz"
# service strace-docker stop

# # copy tracing log
# echo "Copy tracing results"
# cp /var/log/strace-docker/*-*-* /opt/output/tracing/$2_unzip.txt && sleep 2

# # delete cache
# echo "delete cache and lagacy datas"
# echo 3 > /proc/sys/vm/drop_caches
# rm /var/log/strace-docker/*-*-*

set +x