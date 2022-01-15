""" 

cfg.py
====================

Thie module is for making control flow graph
with using collected exploit codes.

Todo:
  * dealing with output file of gcc fdump option
  * extract only basic block with library function
"""

import os
import json
import subprocess

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from tool import Logging
log = Logging.Logging("info")

PERM_OUTPUT_PATH = "/opt/output/perm/"
TEMP_OTUPUT_PATH = "/opt/output/temp/"

EXPLOITDB_PATH = "/exploit/exploit-db/"
PROJZ_PATH = "/exploit/project-zero/"
GIT_PATH = "/exploit/git/"

def get_exploits():
    """get exploit code names and make list.

    Returns:
        eList: eid list

    Raises:
        None: There is no exploit codes
    """
    eList = list()

    with open(f'{PERM_OUTPUT_PATH}exploit.json','r') as f:
        jsonList = json.load(f)
        jsonList.pop(-1)

    eList = list(map(lambda x: [x['EID'],x['src']], jsonList))

    return eList


def make_cfg(eList):
    """making control flow graph from collected exploit codes.

    Args:
        eList(list): List of EID

    Note:
        * Save only *.013t.cfg file in temp output directory
    """
    ############## [START]DEBUG #################
    eList = [('test','exploitdb')]  
    ############## [END]DEBUG ###################
    cwd = os.getcwd()
    os.system('mkdir /tmp/cfg/')
    os.chdir('/tmp/cfg/')
     
    for EID, src in eList:
        # gcc -fdump-tree-cfg-all <target.c>
        if src == "exploitdb":  cmd = f'gcc -fdump-tree-all -w {cwd}{EXPLOITDB_PATH}{EID}.c'
        elif src == "git":      cmd =  f'gcc -fdump-tree-all -w {cwd}{PROJZ_PATH}{EID}.c'
        elif src == "projz":    cmd =  f'gcc -fdump-tree-all -w {cwd}{GIT_PATH}{EID}.c'
        fdump_result = subprocess.check_output(cmd,shell=True).decode()
        if fdump_result == None:
            log.error(f"gcc error - {EID}.c")
            return

        cmd = f'cp {EID}.c.012t.cfg {TEMP_OTUPUT_PATH}'
        mv_result = subprocess.check_output(cmd,shell=True).decode().strip("\n")
        if fdump_result == None:
            log.error(f"move file error - maybe there is no {EID}.c.012t.cfg")
            return

        rm_result = subprocess.check_output('rm *',shell=True).decode().strip("\n")
        if fdump_result == None:
            log.error(f"remove error - maybe there is no a.out")
            return

        log.info(f"made CFG file({EID}.c.012t.cfg) for {EID}.c")
    
    os.chdir(cwd)
    os.system('rm -r /tmp/cfg/')