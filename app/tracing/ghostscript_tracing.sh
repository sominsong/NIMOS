set -x

# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*  2> /dev/null

# eps to png testcase
echo "Tracing Start - eps2png case"
service strace-docker restart
docker run --rm --name gs-container -w /home/ sominsong97/hyper-seccomp:ghostscript bash -c "sleep 1; gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -dGraphicsAlphaBits=4 -sOutputFile=testimage_eps2png.png testimage.eps;"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/ghostscript_eps2png.txt && sleep 2

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*  2> /dev/null

# render at 300 dpi testcase
echo "Tracing Start - render case"
service strace-docker restart
docker run --rm --name gs-container -w /home/ sominsong97/hyper-seccomp:gzip bash -c "sleep 1; gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -r300 -sOutputFile=testimage_300dpi.png testimage.eps;"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/ghostscript_renderdpi.txt && sleep 2

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*  2> /dev/null

# render in grayscale testcase
echo "Tracing Start - render in grayscale case"
service strace-docker restart
docker run --rm --name gs-container -w /home/ sominsong97/hyper-seccomp:gzip bash -c "sleep 1; gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pnggray -sOutputFile=testimage_grayscale.png testimage.pdf;"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/ghostscript_rendergray.txt && sleep 2

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*  2> /dev/null

set +x
