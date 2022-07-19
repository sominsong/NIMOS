set -x

# zip testcase
service strace-docker start
docker run --rm -it -v "$PWD":/home/ -w /home/ myzip sh -c "sleep 2; bzip2 -k test.txt"
service strace-docker stop

# unzip testcase
mv test.txt test.txt.bak
service strace-docker start
docker run --rm -it -v "$PWD":/home/ -w /home/ myzip sh -c "sleep 2; bzip2 -kd test.txt.bz2"
service strace-docker stop

set +x