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
    You can run tests on one application at a time.
    You can test the application through the following options described in Usage and Options.

Usage : 
    ./run.sh -B [-h/-e/-d]

Suboptions :
    -h,                 print help message
    -e [app name],      You can test one of the applications below with this -e option :
                            [mongodb|mysql|httpd|nginx|redis|mariadb|node|tomcat]
    -d [app name],      You can test one of the applications below with this -d option :
                            [gcc|openjdk|gzip|bzip2|qalc|ghostscript|lowriter]
EOF
}

# The function is for shutting down all running containers
function shutdown_all() {
    echo shutdown all containers ...
    running_containers=$(docker ps -a  | awk '{print $1}' |  tail -n+2)
    for i in ${running_containers}; do
        docker rm -f $i &
        echo shutdown $i container
    done
    wait
}

DIR=$(pwd)
echo $DIR

while getopts "hSed" opt; do
    case $opt in
        h)
            help
            exit 0
            ;;
        S)  
            # Pull images
            bash $(pwd)/pull.sh
            # Make tracing folder
            mkdir -p /opt/output/tracing/split
            # Make network
            ## MongoDB
            docker network create mongo_mongo-networks 1> /dev/null
            ## MariaDB
            docker network create mariadb_mariadb-net 1> /dev/null
            ## MySQL
            docker network create mysql_net-mysql 1> /dev/null
            ## Redis
            docker network create redis_redis-net 1> /dev/null

            # Make docker volume
            ## MySQL
            docker volume create mysql_my-db-master 1> /dev/null
            docker volume create mysql_my-db-slave 1> /dev/null

            # Pull folders for bind mounts
            mkdir -p /data/
            git clone -b 28-data-for-docker https://github.com/sominsong/NIMOS.git
            cp -r NIMOS/data/* /data/
            rm -r ./NIMOS/
            ;;
        e)
            if [ $# -ne 2 ] ; then
            	echo "Usage: $0 -e [mongodb|mysql|httpd|nginx|redis|mariadb|node|tomcat]"
                exit 0
            fi
            # shutdow all running containers
            shutdown_all
            echo "Testing $2 ..."
            case $2 in
                "mongodb")
                    # run mongodb containers
                    docker run -d -p 30001:27017 -v /data/mongo/db-01:/data/db --name mongodb-container1 --net mongo-cluster sominsong97/hyper-seccomp:mongo1 &
                    docker run -d -p 30002:27017 -v /data/mongo/db-02:/data/db --name mongodb-container2 --net mongo-cluster sominsong97/hyper-seccomp:mongo2 &
                    docker run -d -p 30003:27017 -v /data/mongo/db-03:/data/db --name mongodb-container3 --net mongo-cluster sominsong97/hyper-seccomp:mongo3 &
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
                    docker run -d -p 3306:3306 -v /data/mysql/db-01:/var/lib/mysql -v /data/mysql/db-01:/var/lib/mysql-files --name mysql-container --net mysql_net-mysql sominsong97/hyper-seccomp:mysql &
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
                    docker run -d -p 6379:6379 --name redis-container1 --net redis_redis-net sominsong97/hyper-seccomp:redis1 &
                    docker run -d -p 6479:6379 --name redis-container2 --net redis_redis-net sominsong97/hyper-seccomp:redis2 &
                    docker run -d -p 6579:6379 --name redis-container3 --net redis_redis-net sominsong97/hyper-seccomp:redis3 &
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
                    docker run -d -p 33306:3306 -v /data/mariadb/db-01:/var/lib/mysql -v /data/mariadb/master/config/:/etc/mysql/conf.d -v /data/mariadb/master/mysql-init-files/:/docker-entrypoint-initdb.d/ --name mariadb-container1 --net mariadb_mariadb-net sominsong97/hyper-seccomp:mariadb1 &
                    docker run -d -p 43306:3306 -v /data/mariadb/db-02:/var/lib/mysql -v /data/mariadb/slave/config/:/etc/mysql/conf.d -v /data/mariadb/slave/mysql-init-files/:/docker-entrypoint-initdb.d/ --name mariadb-container2 --net mariadb_mariadb-net sominsong97/hyper-seccomp:mariadb2 &
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
                    docker run -d --name httpd-container -p 8009:80 sominsong97/hyper-seccomp:myhttpd &
                    wait
                    # setup ftrace
                    bash $(pwd)/app/trace_setup.sh httpd && sleep 1
                    # test
                    bash $(pwd)/app/tracing/httpd_tracing.sh GET && sleep 1
                    bash $(pwd)/app/tracing/httpd_tracing.sh POST && sleep 1
                    bash $(pwd)/app/tracing/httpd_tracing.sh PUT && sleep 1
                    ;;
                "nginx")
                    # run nginx container
                    docker run --name nginx-container -d -p 8009:80 sominsong97/hyper-seccomp:mynginx &
                    wait
                    # setup ftrace
                    bash $(pwd)/app/trace_setup.sh nginx && sleep 1
                    # test
                    bash $(pwd)/app/tracing/nginx_tracing.sh GET && sleep 1
                    bash $(pwd)/app/tracing/nginx_tracing.sh POST && sleep 1
                    bash $(pwd)/app/tracing/nginx_tracing.sh PUT && sleep 1
                    ;;
                "node")
                    # run node container
                    docker run -it -d -p 8000:8000 --name=node-container sominsong97/hyper-seccomp:newnode &
                    wait
                    # setup ftrace
                    bash $(pwd)/app/trace_setup.sh node && sleep 1
                    # test
                    bash $(pwd)/app/tracing/node_tracing.sh GET && sleep 1
                    bash $(pwd)/app/tracing/node_tracing.sh POST && sleep 1
                    ;;
                "tomcat")
                    # run tomcat container
                    docker run -d --name tomcat-test -p 8080:8080 sominsong97/hyper-seccomp:mytomcat &
                    wait
                    # setup ftrace
                    bash $(pwd)/app/trace_setup.sh tomcat && sleep 1
                    # test
                    bash $(pwd)/app/tracing/tomcat_tracing.sh GET && sleep 1
                    bash $(pwd)/app/tracing/tomcat_tracing.sh POST && sleep 1
                    bash $(pwd)/app/tracing/tomcat_tracing.sh PUT && sleep 1
                    ;;
                *)
                    echo "Invalid argument"
                    echo "Usage: $0 -e [mongodb|mysql|httpd|nginx|redis|mariadb|node|tomcat]"
                    exit 1
                    ;;
            esac
            ;;
        d)
            if [ $# -ne 2 ] ; then
            	echo "Usage: $0 -d [gcc|openjdk|gzip|bzip2|qalc|ghostscript|lowriter]"
                exit 0
            fi
            # shutdow all running containers
            shutdown_all
            # remove previous log files
            rm -f /var/log/strace-docker/*-*-*
            echo "Testing $2 ..."
           
            case $2 in
                "gcc")
                    bash $(pwd)/app/tracing/gcc_tracing.sh
                    ;;
                "openjdk")
                    bash $(pwd)/app/tracing/openjdk_tracing.sh
                    ;;
                "gzip")
                    bash $(pwd)/app/tracing/gzip_tracing.sh
                    ;;
                "bzip2")
                    bash $(pwd)/app/tracing/gzip_tracing.sh
                    ;;
                "qalc")
                    bash $(pwd)/app/tracing/qalc_tracing.sh
                    ;;
                "ghostscript")
                    bash $(pwd)/app/tracing/ghostscript_tracing.sh
                    ;;
                "lowriter")
                    bash $(pwd)/app/tracing/lowriter_tracing.sh
                    ;;
                *)
                    echo "Invalid argument"
                    echo "Usage: $0 -d [gcc|openjdk|gzip|bzip2|qalc|ghostscript|lowriter]"
                    exit 1
                    ;;
            esac
            ;;
    esac
done
