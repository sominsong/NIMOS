#!/bin/bash

CUR_DIR=$(pwd)

# Install prerequisites
apt update
apt install -y openssh-server
apt install -y build-essential vim gcc git-all make
apt install -y python3-pip
apt install -y mysql-client-core-8.0 mysql-common

pip install beautifulsoup4


# Install prerequisites for compiling exploit codes
apt install -y libsctp-dev
apt install -y libbluetooth-dev
apt install -y libfuse-dev
apt install -y gcc-multilib g++-multilib
apt install -y libkeyutils-dev
apt install -y libseccomp-dev
apt install -y kernel-package
apt install -y libasm-dev
apt-get install -y linux-headers-generic

git clone https://github.com/thradams/conio.git
mv conio/ /opt/
cd /opt/conio
make

cp conio.h ${CUR_DIR}/exploit/exploit-db/

cd ${CUR_DIR}