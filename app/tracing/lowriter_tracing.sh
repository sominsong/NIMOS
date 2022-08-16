set -x

# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

# doc to pdf testcase
echo "Tracing Start - doc2pdf case"
service strace-docker restart
docker run --rm --name lw-container -w /home/ sominsong97/hyper-seccomp:lowriter bash -c "sleep 1; lowriter --convert-to pdf *.doc;"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

# odt to pdf testcase
echo "Tracing Start - odf2pdf case"
service strace-docker restart
docker run --rm --name lw-container -w /home/ mylowriter bash -c "sleep 1; lowriter --convert-to pdf *.odt;"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

# doc to txt testcase
echo "Tracing Start - doc2txt"
service strace-docker restart
docker run --rm --name lw-container -w /home/ mylowriter bash -c "sleep 1; lowriter --convert-to 'txt:Text (encoded):UTF8' *.doc;"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

set +x