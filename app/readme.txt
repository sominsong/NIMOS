-------<컨테이너 실행>-------

1) mongodb

1-1) mongodb docker volume 설정
$ mkdir -p /data/mongo/db-01
$ mkdir -p /data/mongo/db-02
$ mkdir -p /data/mongo/db-03

1-2) mongodb 컨테이너 생성
# docker [command] [-d: detach 모드] [-p: 포트 바인딩] [-v: 볼륨 연결] [--name: 컨테이너 이름] [--net: 도커 네트워크 이름] [이미지:버전]
# mongod [--replSet: Replica Set 이름][--dbpath: 데이터베이스 경로]
$ docker run -d -p 30001:27017 -v /data/mongo/db-01:/data/db --name mongodb-container1 --net mongo-cluster mongo\
  mongod --replSet mongo-repl --dbpath /data/db 
$ docker run -d -p 30002:27017 -v /data/mongo/db-02:/data/db --name mongodb-container2 --net mongo-cluster mongo mongod --replSet mongo-repl --dbpath /data/db
$ docker run -d -p 30003:27017 -v /data/mongo/db-03:/data/db --name mongodb-container3 --net mongo-cluster mongo mongod --replSet mongo-repl --dbpath /data/db

1-4) container1의 mongodb 컨테이너 접속해서 mongo 명령어 실행
$ docker exec -it mongodb-container1 mongo

1-5) 이 후 Primary-Secondary 설정 및 Replica Set 설정 (db 이름: ycsb)
# https://code-machina.github.io/2019/07/17/Mongo-and-Docker-Part-1.html#section-1 사이트 참고

2) mysql

2-1) database 'test' table 'test' 만들기
$ mysql> CREATE DATABASE test;
$ mysql> CREATE TABLE test (id int NOT NULL auto_increment primary key, name VARCHAR(15) NOT NULL, phone VARCHAR(15) NOT NULL);

3) redis

3-1) network 구성
$ docker network create radis-net

3-2) docker-compose로 docker 띄우기
https://sup2is.github.io/2020/07/22/redis-replication-with-sentinel.html 사이트 참고
$ docker-compose up -d

4) mariadb

4-1) network 구성
$ docker network create mariadb-net

4-2) volume 설정
$ mkdir -p /data/mariadb/db

4-3) docker-compose로 docker 띄우기
# 작동 안될 경우 line-by-line으로 실행시키기
$ source run.sh 

4-4) table 'test' 만들기
$ MariaDB [test]> CREATE TABLE test (id int NOT NULL auto_increment primary key, name VARCHAR(15) NOT NULL, phone VARCHAR(15) NOT NULL);


5) apache

5-1) Dockerfile 경로에서 myapache 이미지 생성
$ docker build -t myapache .

5-2)방금 만든 myapache 이미지를 통해 apache 컨테이너 실행
$ docker run -d --name apache-container -p 8009:80 myapache


6) nginx

6-1) nginx index.html 만들기
$ vi /data/nginx/html/index.html

6-2) nginx 컨테이너 실행
$ docker run --name nginx-container -v /data/nginx/html:/usr/share/nginx/html -d -p 8009:80 nginx:latest

7) node

7-1) node.js 웹 소스 작성
$ touch nodejs_test.js # 8000번 포트에서 접속 가능

7-2) node 컨테이너 실행
$ docker run -it -d -p 8000:8000 --name=node-container node:15.12.0-alpine3.12

<GET test>
7-3) 소스 코드 컨테이너 내부로 복사
$ docker cp nodejs_test.js node-container:/nodejs_test.js

7-4) node 서버 실행 for GET test
$ docker exec -d node-container /bin/sh -c "node nodejs_test.js"

<POST test>
7-3) 소스 코드 컨테이너 내부로 복사
$ docker cp POST_test.js node-container:/nodejs_test.js

7-4) node 서버 실행 for POST test
$ docker exec -d node-container /bin/sh -c "node nodejs_test.js"

8) tomcat

8-1) tomcat 컨테이너 실행
$ docker run -d --name tomcat-container -p 8080:8080 tomcat:latest

8-2) war 파일 컨테이너 안으로 복사
$ docker cp sample.war tomcat-container:/usr/local/tomcat/webapps

9) gcc / openjdk
# strace-docker 이용해서 tracing
# 결과 /var/log/strace-docker에 저장됨




-------<shell script 실행 순서>-------

젤 먼저, docker 하나만 띄워놓고 ftrace 설정 setup
$ bash trace_setup.sh ${tracing_image_name}


1) mongodb
# tracing CRUD
$ bash mongo_tracing.sh ${C/R/U/D}

2) mysql
# tracing CRUD (cf. Warning 떠도 상관 없음)
$ bash mysql_tracing.sh ${C/R/U/D}

3) redis
# tracing CRUD
$ bash redis_tracing.sh ${C/R/U/D}

4) mariadb
# tracing CRUD
$ bash mariadb_tracing.sh ${C/R/U/D}

4) httpd
# tracing METHOD
$ bash httpd_tracing.sh ${GET/POST/PUT} 

5) nginx
# tracing METHOD
$ bash nginx_tracing.sh ${GET/POST/PUT} 

6) node
# tracing METHOD
$ bash node_tracing.sh ${GET/POST}

7) tomcat
# tracing METHOD
$ bash tomcat_tracing.sh ${GET/POST/PUT}

