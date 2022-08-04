#!bin/bash

####################### <app.sh> #######################
# 
# This shell script is for extracting the system call sequences
# from the execution of a normally operating application.
# 
########################################################

# option error handling
if [[ $# -lt 1 ]]; then
    echo "app.sh must have OPTS [ARGS]"
    echo "Try bash app.sh -h for more information."
	exit 1
fi

# help option
function help() {
/bin/cat << EOF

Help :
    Before running the test, you MUST set it up through the -S option.
    You can run tests on one application at a time.
    You can test the application through the following options described in Usage and Options.

Usage : 
    ./run.sh [-h -S -A -B]

Options :
    -h,                 print help message
    -A [app name],      You can test one of the applications below with this -A option :
                            [mongodb|mysql|httpd|nginx|redis|mariadb|node|tomcat]
    -B [app name],      You can test one of the applications below with this -B option :
                            [gcc|openjdk|gzip|bzip2|qalc|ghostscript|lowriter]
    -S,                 Setup for testing
EOF
}

# The function is for shutting down all running containers
function shutdown_all() {
    # 
    running_containers=$(docker ps  | grep 'Up' |awk '{print $1}')
    for i in ${running_containers}; do
        docker rm -f $i
    done
}


while getopts "hASB" opt; do
    case $opt in
        h)
            help
            exit 0
            ;;
        S)    
            # Make network
            ## MongoDB
            docker network create mongo_mongo-networks
            ## MariaDB
            docker network create mariadb_mariadb-net
            ## MySQL
            docker network create mysql_net-mysql
            ## Redis
            docker network create redis_redis-net

            # Make docker volume
            ## MySQL
            docker volume create mysql_my-db-master
            docker volume create mysql_my-db-slave

            # Make local folders for bind mounts
            mkdir -p /data/mongo/db-01 /data/mongo/db-02 /data/mongo/db-03
            mkdir -p /data/mariadb/db-01 /data/mariadb/db-02
            mkdir -p /data/redis/db-01 /data/redis/db-02
            mkdir -p /data/gcc
            ;;
        A)
            if [ $# -ne 2 ] ; then
            	echo "Usage: $0 -A [mongodb|mysql|httpd|nginx|redis|mariadb|node|tomcat]"
                exit 0
            fi
            # shutdow all running containers
            shutdown_all
            echo "Testing $2 ..."
            case $2 in
                "mongodb")
                    # run mongodb containers
                    docker run -d -p 30001:27017 -v /data/mongo/db-01:/data/db --name mongodb-container1 --net mongo_mongo-networks sominsong97/hyper-seccomp:mymongo mongod --replSet mongo-repl --dbpath /data/db &
                    docker run -d -p 30002:27017 -v /data/mongo/db-02:/data/db --name mongodb-container2 --net mongo_mongo-networks sominsong97/hyper-seccomp:mymongo mongod --replSet mongo-repl --dbpath /data/db &
                    docker run -d -p 30003:27017 -v /data/mongo/db-03:/data/db --name mongodb-container3 --net mongo_mongo-networks sominsong97/hyper-seccomp:mymongo mongod --replSet mongo-repl --dbpath /data/db &
                    wait
                    # setup ftrace
                    bash $(pwd)/app/trace_setup.sh mongodb && sleep 1
                    # test
                    bash $(pwd)/app/tracing/mongodb_tracing.sh D && sleep 1
                    bash $(pwd)/app/tracing/mongodb_tracing.sh C && sleep 1
                    bash $(pwd)/app/tracing/mongodb_tracing.sh R && sleep 1
                    bash $(pwd)/app/tracing/mongodb_tracing.sh U && sleep 1
                    ;;
                "mysql")
                    # run mysql containers
                    docker run -d -p 3306:3306 -v mysql_my-db-master:/var/lib/mysql --name mysql_db-master --net mysql_net-mysql sominsong97/hyper-seccomp:mysql_master &
                    docker run -d -p 3307:3306 -v mysql_my-db-slave:/var/lib/mysql --name mysql_db-slave --net mysql_net-mysql sominsong97/hyper-seccomp:mysql_slave &
                    wait
                    # setup ftrace
                    bash $(pwd)/app/trace_setup.sh mysql && sleep 1
                    # test
                    bash $(pwd)/app/tracing/mysql_tracing.sh D && sleep 1
                    bash $(pwd)/app/tracing/mysql_tracing.sh C && sleep 1
                    bash $(pwd)/app/tracing/mysql_tracing.sh R && sleep 1
                    bash $(pwd)/app/tracing/mysql_tracing.sh U && sleep 1   
                    ;;
                "redis")
                    # run redis containers
                    docker run -d --net redis_redis-net -v /data/redis/db-01:/data/db -p 6379:6379 --name redis-master sominsong97/hyper-seccomp:myredis &
                    docker run -d --net redis_redis-net -v /data/redis/db-02:/data/db -p 6479:6479 --name redis-slave sominsong97/hyper-seccomp:myredis &
                    wait
                    # setup ftrace
                    bash $(pwd)/app/trace_setup.sh redis && sleep 1
                    # test
                    bash $(pwd)/app/tracing/redis_tracing.sh D && sleep 1
                    bash $(pwd)/app/tracing/redis_tracing.sh C && sleep 1
                    bash $(pwd)/app/tracing/redis_tracing.sh R && sleep 1
                    bash $(pwd)/app/tracing/redis_tracing.sh U && sleep 1
                    ;;
                "mariadb")
                    # run mariadb containers
                    docker run -d --net mariadb_mariadb-net -v /data/mariadb/db-01:/var/lib/mysql -p 33306:3306 --name mariadb-master sominsong97/hyper-seccomp:mymariadb &
                    docker run -d --net mariadb_mariadb-net -v /data/mariadb/db-02:/var/lib/mysl -p 43306:3306 --name mariadb-slave sominsong97/hyper-seccomp:mymariadb &
                    wait
                    # setup ftrace
                    bash $(pwd)/app/trace_setup.sh mariadb && sleep 1
                    # test
                    bash $(pwd)/app/tracing/mariadb_tracing.sh D && sleep 1
                    bash $(pwd)/app/tracing/mariadb_tracing.sh C && sleep 1
                    bash $(pwd)/app/tracing/mariadb_tracing.sh I && sleep 1
                    bash $(pwd)/app/tracing/mariadb_tracing.sh R && sleep 1
                    bash $(pwd)/app/tracing/mariadb_tracing.sh U && sleep 1
                    ;;
                "httpd")
                    # run httpd container
                    docker run -d --name httpd-container -p 8009:80 sominsong97/hyper-seccomp:myhttpd && sleep 1
                    # setup ftrace
                    bash $(pwd)/app/trace_setup.sh httpd && sleep 1
                    # test
                    bash $(pwd)/app/tracing/httpd_tracing.sh GET && sleep 1
                    bash $(pwd)/app/tracing/httpd_tracing.sh POST && sleep 1
                    bash $(pwd)/app/tracing/httpd_tracing.sh PUT && sleep 1
                    ;;
                "nginx")
                    # run nginx container
                    docker run --name nginx-container -d -p 8009:80 sominsong97/hyper-seccomp:mynginx && sleep 1
                    # setup ftrace
                    bash $(pwd)/app/trace_setup.sh nginx && sleep 1
                    # test
                    bash $(pwd)/app/tracing/nginx_tracing.sh GET && sleep 1
                    bash $(pwd)/app/tracing/nginx_tracing.sh POST && sleep 1
                    bash $(pwd)/app/tracing/nginx_tracing.sh PUT && sleep 1
                    ;;
                "node")
                    # run node container
                    docker run -it -d -p 8000:8000 --name=node-container sominsong97/hyper-seccomp:newnode && sleep 1
                    # setup ftrace
                    bash $(pwd)/app/trace_setup.sh node && sleep 1
                    # test
                    bash $(pwd)/app/tracing/node_tracing.sh GET && sleep 1
                    bash $(pwd)/app/tracing/node_tracing.sh POST && sleep 1
                    ;;
                "tomcat")
                    # run tomcat container
                    docker run -d --name tomcat-test -p 8080:8080 sominsong97/hyper-seccomp:mytomcat && sleep 1
                    # setup ftrace
                    bash $(pwd)/app/trace_setup.sh tomcat && sleep 1
                    # test
                    bash $(pwd)/app/tracing/tomcat_tracing.sh GET && sleep 1
                    bash $(pwd)/app/tracing/tomcat_tracing.sh POST && sleep 1
                    bash $(pwd)/app/tracing/tomcat_tracing.sh PUT && sleep 1
                    ;;
                *)
                    echo "Invalid argument"
                    echo "Usage: $0 -A [mongodb|mysql|httpd|nginx|redis|mariadb|node|tomcat]"
                    exit 1
                    ;;
            esac
            ;;
        B)
            if [ $# -ne 2 ] ; then
            	echo "Usage: $0 -B [gcc|openjdk|gzip|bzip2|qalc|ghostscript|lowriter]"
                exit 0
            fi
            echo "Testing $2 ..."
            case $2 in
                "gcc")
                    service strace-docker start
                    docker run --rm sominsong97/hyper-seccomp:mygcc bash -c "sleep 5; gcc -o myapp main.c;"
                    service strace-docker stop
                    ;;
                "openjdk")
                    service strace-docker start
                    service strace-docker stop
                    ;;
                "gzip")
                    # zip testcase
                    service strace-docker start
                    docker run --rm -it -w /home/ sominsong97/hyper-seccomp:myzip sh -c "sleep 2; bzip2 -k test.txt"
                    service strace-docker stop
                    service strace-docker start
                    docker run --rm -it -w /home/ myzip sh -c "sleep 2; bzip2 -kd test.txt.bz2"
                    service strace-docker stop
                    ###옮기는 거 코드 짜야함!
                    ;;
                "qalc")
                    service strace-docker start
                    service strace-docker stop
                    ;;
                "ghostscript")
                    service strace-docker start
                    service strace-docker stop
                    ;;
                "lowriter")
                    service strace-docker start
                    service strace-docker stop
                    ;;
                *)
                    echo "Invalid argument"
                    echo "Usage: $0 -B [gcc|openjdk|gzip|bzip2|qalc|ghostscript|lowriter]"
                    exit 1
                    ;;
            esac
            ;;
    esac
done