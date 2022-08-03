CREATE DATABASE test;

#create masteruser and grant privileges
create user test@'%' identified by 'password';
grant all privileges on test.* to test@'%' identified by 'password';

## flush
flush privileges;