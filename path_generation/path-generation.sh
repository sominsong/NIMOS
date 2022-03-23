#!/bin/bash

set -ex

CUR_PATH=$(pwd)
. $(pwd)/common.conf

# clear
rm -fv ${OUT_PRM_DIR}path/*.json
rm -fv ${OUT_TMP_DIR}*.cfg
rm -fv ${OUT_TMP_DIR}*.original

# run in turn
sudo python3 -B ${CUR_PATH}/path_generation/path.py