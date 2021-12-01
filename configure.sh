#!/bin/bash

CUR_DIR=$(pwd)

# Install prerequisites
sudo apt update
sudo apt install -y openssh-server
sudo apt install -y build-essential vim gcc git
sudo apt install -y python3-pip

sudo pip install beautifulsoup4

# Install prerequisites for compiling exploit codes
