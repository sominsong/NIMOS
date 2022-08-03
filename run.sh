#!/bin/bash

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
    -A,     run all
    -C,     crawling exploit codes
    -P,     path generation
    -S,     syscall generation
    -N,     N-gram analysis
    -B,     Benign application test
EOF
}


while getopts "hCAPSMN" opt; do
    case $opt in
        h)
            help
            exit 0
            ;;
        A)  
            bash ${SYSCALL_DIR}syscall-generation.sh
            bash ${PATH_DIR}path-generation.sh
            echo CVE-syscall mapping
            ;;
        C)
            echo Crawling Exploit Codes
            bash ${EXPLOIT_DIR}exploit.sh
            ;;
        S)
            echo Syscall Generation
            bash ${SYSCALL_DIR}syscall-generation.sh
            ;;
        P)
            echo Path Generation
            bash ${PATH_DIR}path-generation.sh
            ;;
        N)
            echo N-gram Analysis
            python3 -B ${ANALYSIS_DIR}ngram.py
            ;;
        B)
            echo Benign Application Test
            bash ${APP_DIR}app.sh
        
    esac
done