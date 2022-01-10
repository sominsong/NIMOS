""" 

Graph.py
====================

Thie class is for graph representation.

Todo:
  * 
"""

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from tool import Logging
log = Logging.Logging("info")

from collections import deque

class Graph:

    def __init__(self, funcNm, vList):
        self.funcNm = funcNm
        self.V = []
        self.E = [(0,2)]
        self.vList = vList
        self.vNum = 2
        self.loop = []
        self.path = []

    def add_vertex(self, v):
        self.V.append(v.bbNum)
        self.vList.append(v)
        self.vNum += 1
    
    def add_edge(self, e):
        self.E.append(e)

    def add_loop(self, start, end):
        self.loop = [start, end]

    def find_edge(self, V, visited):
        eList = []
    
        for frm, to in self.E:
            if frm == V:
                eList.append(to)
        eList.sort()
        if len(eList) == 1:
            return eList
        else:            
            for E in eList:
                if E in visited and not E == self.loop[0]:
                    eList.remove(E)
                else:
                    continue
            return eList

        return []

    def DFS(self):
        to = []      # vertex list to visit
        done = []    # vertex list already visited
        path = []           # vertex path

        to.append(0)

        while to:
            Vfrom = to.pop()
            done.append(Vfrom)
            path.append(Vfrom)
            Vto = self.find_edge(Vfrom, done)
            log.debug(f"Vfrom: {Vfrom}\n\tVto: {Vto}\n\tdone: {done}\n\tto: {to}\n\tpath: {path}\n")
            if Vto:
                to.extend(Vto)
            else:
                if Vfrom == 1:  # finish with reaching the exit node
                    self.path.append(path.copy())
                    log.debug(f"PATH : {path}")
                    if not to:
                        return
                    else:
                        while path:
                            V = path.pop()
                            if to[-1] in self.find_edge(V, done):
                                path.append(V)
                                break
                            else:
                                done.remove(V)
                else:   # finish without reaching the exit node
                    if not to:
                        self.path.append(path.copy())
                        log.debug(f"PATH : {path}")
                        return
                    else:
                        self.path.append(path.copy())
                        log.debug(f"PATH : {path}")
                        while path:
                            V = path.pop()
                            if to[-1] in self.find_edge(V, done):
                                path.append(V)
                                break
                            else:
                                done.remove(V)