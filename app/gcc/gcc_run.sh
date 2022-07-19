service strace-docker start
docker run --rm -v "$PWD":/home/ -w /home/ mygcc bash -c "sleep 5; gcc -o myapp main.c;"
service strace-docker stop


# docker run --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp mygcc gcc -o main main.c

# docker run --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp gcc:4.9 gcc -o main main.c; 