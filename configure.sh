#!/bin/bash

CUR_DIR=$(pwd)

# Install prerequisites
sudo apt update
sudo apt install -y openssh-server
sudo apt install -y build-essential vim gcc git
sudo apt install -y python3-pip

# Install prerequisites for compiling exploit codes
