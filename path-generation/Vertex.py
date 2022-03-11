""" 

Vertex.py
====================

Thie class is for vertex representation.

Todo:
  * 
"""

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from tool import Logging
log = Logging.Logging("info")

TEST_PATH = "/opt/output/temp/testcase/result/"

class Vertex:

    def __init__(self, bbNum, funcList):
        self.bbNum = bbNum
        self.funcList = funcList
        self.syscallList = list()

    def make_syscallList(self, EID, funcNm):
      if self.funcList:
        for API in self.funcList:
          if os.path.isfile(f"{TEST_PATH}{API}-{EID}-{funcNm}.txt"):
            with open(f"{TEST_PATH}{API}-{EID}-{funcNm}.txt", "r") as f:
              sysSeq = f.readlines()
              for syscall in sysSeq:
                self.syscallList.append(syscall.strip())
          else:
            if os.path.isfile(f"{TEST_PATH}{API}-default-default.txt"):
              with open(f"{TEST_PATH}{API}-default-default.txt", "r") as f:
                sysSeq = f.readlines()
                for syscall in sysSeq:
                  self.syscallList.append(syscall.strip())
            else:
              # log.info(f"No syscall sequence - {API}")
              self.syscallList.append(API)