CREATE DATABASE test;

#create masteruser and grant privileges
create user test@'%' identified by 'admin';
grant all privileges on test.* to test@'%' identified by 'admin';

## flush
flush privileges;