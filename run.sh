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
    ./run.sh [-h -A -C -P -S -M]

Options :
    -h,     print help message
    -A,     run all
    -C,     crawling exploit codes
    -P,     path generation
    -S,     syscall generation
    -M,     CVE-syscall mapping
EOF
}


while getopts "hCAPSM" opt; do
    case $opt in
        h)
            help
            exit 0
            ;;
        C)
            echo Crawling Exploit Codes
            bash ${EXPLOIT_DIR}exploit.sh
            ;;
        A)
            echo Path Generation
            echo Syscall Generation
            echo CVE-syscall mapping
            ;;
        P)
            echo Path Generation
            ;;
        S)
            echo Syscall Generation
            ;;
        M)
            echo CVE-syscall mapping
            ;;
        
    esac
done