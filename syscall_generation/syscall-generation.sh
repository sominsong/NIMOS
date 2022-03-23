#!/bin/bash

set -ex

CUR_PATH=$(pwd)
. $(pwd)/common.conf

# clear
rm -fv ${OUT_TMP_DIR}testcase/result/*
rm -fv ${OUT_TMP_DIR}testcase/*-*-*

# run in turn
sudo python3 -B ${CUR_PATH}/path_generation/cfg.py
sudo python3 -B ${CUR_PATH}/syscall_generation/usecase.py
sudo python3 -B ${CUR_PATH}/syscall_generation/testcase.py