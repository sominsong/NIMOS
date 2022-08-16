CREATE DATABASE test; 

##create masteruser and grant privileges
grant all privileges on test.* to dbname@'%' identified by 'admin';

#replication
grant replication slave on *.* to 'test'@'%';

## flushj
flush privileges;