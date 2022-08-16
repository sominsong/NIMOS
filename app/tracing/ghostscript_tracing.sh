set -x

# delete cache
echo "delete cache..."
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

# eps to png testcase
echo "Tracing Start - eps2png case"
service strace-docker restart
docker run --rm --name gs-container -w /home/ sominsong97/hyper-seccomp:ghostscript sh -c "sleep 1; gs  -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -dGraphicsAlphaBits=4 -sOutputFile=testimage_eps2png.png testimage.eps;"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/ghostscript_eps2png.txt && sleep 2

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

# render at 300 dpi testcase
echo "Tracing Start - render case"
service strace-docker restart
docker run --rm --name gs-container -w /home/ sominsong97/hyper-seccomp:gzip sh -c "sleep 1; gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -r300 -sOutputFile=testimage_300dpi.png testimage.eps;"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/ghostscript_renderdpi.txt && sleep 2

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

# render in grayscale testcase
echo "Tracing Start - render in grayscale case"
service strace-docker restart
docker run --rm --name gs-container -w /home/ sominsong97/hyper-seccomp:gzip sh -c "sleep 1; gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pnggray -sOutputFile=testimage_grayscale.png testimage.pdf;"
service strace-docker stop

# copy tracing log
echo "Copy tracing results"
cp /var/log/strace-docker/*-*-* /opt/output/tracing/ghostscript_rendergray.txt && sleep 2

# delete cache
echo "delete cache and lagacy datas"
echo 3 > /proc/sys/vm/drop_caches
rm /var/log/strace-docker/*-*-*

set +x
