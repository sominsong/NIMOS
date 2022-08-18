set -x

# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*  2> /dev/null

# doc to pdf testcase
echo "Tracing Start - doc2pdf case"
service strace-docker restart
docker run --rm --name lw-container -w /home/ sominsong97/hyper-seccomp:lowriter bash -c "sleep 1; lowriter --convert-to pdf *.doc;"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/lowriter_doc2pdf.txt && sleep 2

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*  2> /dev/null

# odt to pdf testcase
echo "Tracing Start - odf2pdf case"
service strace-docker restart
docker run --rm --name lw-container -w /home/ sominsong97/hyper-seccomp:lowriter bash -c "sleep 1; lowriter --convert-to pdf *.odt;"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/lowriter_odt2pdf.txt && sleep 2

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*  2> /dev/null

# doc to txt testcase
echo "Tracing Start - doc2txt"
service strace-docker restart
docker run --rm --name lw-container -w /home/ sominsong97/hyper-seccomp:lowriter bash -c "sleep 1; lowriter --convert-to 'txt:Text (encoded):UTF8' *.doc;"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/lowriter_doc2txt.txt && sleep 2

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*  2> /dev/null

set +x