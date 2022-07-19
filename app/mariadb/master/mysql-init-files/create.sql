CREATE DATABASE test; 

##create masteruser and grant privileges
grant all privileges on test.* to dbname@'%' identified by 'password';

#replication
grant replication slave on *.* to 'test'@'%';

## flushj
flush privileges;