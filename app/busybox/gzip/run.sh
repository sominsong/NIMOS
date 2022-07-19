# zip
service strace-docker restart
docker run --rm --name gzip-container  -v "$PWD":/home/ -w /home/ mygzip sh -c "sleep 2; gzip *.txt"

# unzip
service strace-docker restart
docker run --rm --name gzip-container  -v "$PWD":/home/ -w /home/ mygzip sh -c "sleep 2; gzip -d *.gz"
