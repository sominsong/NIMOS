""" 

cfg.py
====================

Thie module is for making control flow graph
with using collected exploit codes.

Todo:
  * dealing with output file of gcc fdump option
  * extract only basic block with library function
"""

import re
import json
import subprocess

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tool import Logging
log = Logging.Logging("info")

from compile_option import coption

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

<<<<<<< HEAD:path-generation/cfg.py
    return eList        

=======
    return eList
>>>>>>> ba2792eff59deea85212ad90cd7b49c345f6cb24:path_generation/cfg.py


def make_cfg(eList):
    """making control flow graph from collected exploit codes.

    Args:
        eList(list): List of EID

    Note:
        * Save only *.c.013t.cfg file and *.c.004t.original in temp output directory
    """

    cwd = os.getcwd()
    os.system('mkdir /tmp/cfg/')
    os.chdir('/tmp/cfg/')
    opt = ""
     
    for EID, src in eList:

        if not os.path.isfile(f"{cwd}{EXPLOITDB_PATH}{EID}.c"):
            log.warning(f"{EID} file is not c file. Maybe .sh/.txt/.md/.rb etc.")
            continue

        # get gcc compile option
        if coption.get(EID): opt = coption.get(EID) 
        # gcc -fdump-tree-cfg-all <target.c>
        if src == "exploitdb":  cmd = f'gcc -static -fno-builtin -fdump-tree-all -w {cwd}{EXPLOITDB_PATH}{EID}.c {opt} -O3 2>/tmp/error.txt'
        elif src == "git":      cmd =  f'gcc -static -fno-builtin -fdump-tree-all -w {cwd}{PROJZ_PATH}{EID}.c {opt} 2>/tmp/error.txt'
        elif src == "projz":    cmd =  f'gcc -static -fno-builtin -fdump-tree-all -w {cwd}{GIT_PATH}{EID}.c {opt} 2>/tmp/error.txt'
        opt = ""
        try:
            fdump_result = subprocess.check_output(cmd,shell=True).decode()
        except Exception as e:
            log.error(f"Compile Error - {EID}")
            continue
        # copy cfg and original
        cmd = f'cp {EID}.c.012t.cfg {EID}.c.004t.original {TEMP_OTUPUT_PATH}'
        mv_result = subprocess.check_output(cmd,shell=True).decode().strip("\n")
        if mv_result == None:
            log.error(f"move file error - maybe there is no {EID}.c.012t.cfg or {EID}.c.004t.original")
            continue

        rm_result = subprocess.check_output('rm *',shell=True).decode().strip("\n")
        if rm_result == None:
            log.error(f"remove error - maybe there is no a.out")
            continue

        log.info(f"made CFG file({EID}.c.012t.cfg, {EID}.c.004t.original) for {EID}.c")
    
    os.chdir(cwd)
    os.system('rm -r /tmp/cfg/')

if __name__ == "__main__":
    
    eList = get_exploits()
    make_cfg(eList)