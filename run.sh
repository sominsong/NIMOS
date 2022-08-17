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
    -B,     benign application test (You must manually test the application.)
    -R,     parsing benign application test result (You must execute it after -B option.)
EOF
}


while getopts "hACSPNBR" opt; do
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
            echo "You have to manually test the application.\n Options can be executed with -B and -R."
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
             echo Benign Application Test
            if [ $# -lt 2 ] ; then
                echo How to Run Application Test
                bash ${APP_DIR}app.sh -S
                bash ${APP_DIR}app.sh -h
                exit 0
            fi
            if [ $# -eq 3 ] ; then
                case $2 in
                    "-e")
                        bash ${APP_DIR}app.sh -e $3
                        ;;
                    "-d")
                        bash ${APP_DIR}app.sh -d $3
                        ;;
                esac
                exit 0
            fi
            bash ${APP_DIR}app.sh -h
            ;;
        R)
            echo "Parsing Benign Application Test Result"
            python3 -B ${APP_DIR}parsingPerThread.py
            python3 -B ${APP_DIR}parsing.py
            ;;
    esac
done