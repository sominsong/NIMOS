#!bin/bash

####################### <run.sh> #######################
# 
# This shell script is for runnning node container image
# If the code below does not work properly,
# manually run it line by line.
# 
########################################################

set -x

# Run node container
docker run -it -d -p 8000:8000 --name=node-container node:15.12.0-alpine3.12
# Copy source code into container for GET testcase
docker cp nodejs_test.js node-container:/nodejs_test.js
# Copy source code into container for POST testcase
$ docker cp POST_test.js node-container:/nodejs_test.js

set +x