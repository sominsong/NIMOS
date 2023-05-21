#!/bin/bash

CUR_DIR=$(pwd)

# Install prerequisites
apt update
apt-get update
apt install -y openssh-server
apt install -y build-essential vim gcc git-all make
apt install -y python3-pip
apt install -y trace-cmd

pip install beautifulsoup4
pip install requests

# Install Docker
apt-get install -y ca-certificates curl gnupg lsb-release
## Add Docker's official GPC Key
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
## Install Docker Engine
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
VERSION_STRING=$(apt-cache madison docker-ce | awk '{print $3}' | sed -n '1p')
apt-get install -y docker-ce=${VERSION_STRING} docker-ce-cli=${VERSION_STRING} containerd.io docker-compose-plugin
docker run hello-world

# Install prerequisities for testing docker applciations
apt install -y mongodb-clients mysql-client-core-8.0 mysql-common
apt install -y apache2-utils redis-tools


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

# Install strace-docker for tracing container
git clone https://github.com/amrabed/strace-docker && ./strace-docker/install
mv strace-docker/ /opt/
service strace-docker status
