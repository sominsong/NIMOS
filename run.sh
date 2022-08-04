#!/bin/bash

####################### <run.sh> #######################
# 
# This shell script is for controling the overall system operation.
# The system can be operated through the options that can be seen 
# through the -h option.
# 
########################################################

set -e

# option error handling
if [[ $# -lt 1 ]]; then
    echo "run.sh must have OPTS [ARGS]"
    echo "Try bash run.sh -h for more information."
	exit 1
fi

. $(pwd)/common.conf

function help() {
/bin/cat << EOF

Usage : 
    ./run.sh [-h -A -C -P -S -N -B]

Options :
    -h,     print help message
    -A,     run all [Default Option]
    -C,     crawling exploit codes
    -P,     path generation
    -S,     syscall generation
    -N,     N-gram analysis
    -B,     Benign application test (You have to manually test the application.)
EOF
}


while getopts "hACSPNB" opt; do
    case $opt in
        h)
            help
            exit 0
            ;;
        A)  
            echo Crawling Exploit Codes
            bash ${EXPLOIT_DIR}exploit.sh
            echo Finished Crawling Exploit Codes
            
            echo Syscall Generation
            bash ${SYSCALL_DIR}syscall-generation.sh
            echo Finished generating syscall

            echo Path Generation
            bash ${PATH_DIR}path-generation.sh
            echo Finished generating path
            
            echo N-gram Analysis
            python3 -B ${ANALYSIS_DIR}ngram.py
            echo Finished N-gram Analysis

            echo Benign pplication Test
            bash ${APP_DIR}app.sh -h
            echo "You have to manually test the application.\n Options can be executed with -B."
            ;;
        C)
            echo Crawling Exploit Codes
            bash ${EXPLOIT_DIR}exploit.sh
            ;;
        P)
            echo Path Generation
            bash ${PATH_DIR}path-generation.sh
            ;;
        S)
            echo Syscall Generation
            bash ${SYSCALL_DIR}syscall-generation.sh
            ;;
        N)
            echo N-gram Analysis
            python3 -B ${ANALYSIS_DIR}ngram.py
            ;;
        B)
            if [ $# -ne 2 ] ; then
                echo How to Run Application Test
                # bash ${APP_DIR}app.sh -S
                # bash ${APP_DIR}app.sh -h
                exit 0
            fi
            echo hello
        
    esac
done