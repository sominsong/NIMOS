#!/bin/bash

CUR_DIR=$(pwd)

# Install prerequisites
sudo apt update
sudo apt install -y openssh-server
sudo apt install -y build-essential vim gcc git
sudo apt install -y python3-pip

sudo pip install beautifulsoup4

# Install prerequisites for compiling exploit codes
sudo apt install -y libsctp-dev
sudo apt install -y libbluetooth-dev
sudo apt install -y libfuse-dev
sudo apt install -y gcc-multilib g++-multilib
sudo apt install -y libkeyutils-dev
sudo apt install -y libseccomp-dev
sudo apt install -y kernel-package
sudo apt install -y libasm-dev
sudo apt-get install -y linux-headers-generic

sudo git clone https://github.com/thradams/conio.git
sudo /opt/conio/make
cp /opt/conio/conio.h $(pwd)/exploit/exploit-db/