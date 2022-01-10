#!/bin/bash

set -ex

CUR_PATH=$(pwd)

# run in turn
sudo python3 -B ${CUR_PATH}/path-generation/cfg.py
sudo python3 -B ${CUR_PATH}/path-generation/path.py