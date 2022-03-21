""" 

Graph.py
====================

Thie class is for graph representation.

Todo:
  * more than 2 Loop processing
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
        self.vList = vList.copy()
        self.vNum = 2
        self.loop = dict()  # for DFS
        self.MAX_LOOP = 3
        self.visit = {0:False, 1:False, 2:False}   # for DFS
        self.edge = dict()  # for DFS
        self.stack = []     # for DFS
        self.path = []  # bb path
        self.syscallpath = []
        self.newsyspath = []

    def add_vertex(self, v):
        self.V.append(v.bbNum)
        self.vList.append(v)
        self.vNum += 1
        self.visit[v.bbNum] = False
    
    def add_edge(self, e):
        self.E.append(e)

    def add_loop(self, v):
        if not v in self.loop:
            # self.loop[v] = False
            self.loop[v] = 0
 
    def prepare_DFS(self):
        # make edge dictionary {e: [connected edge list], ...}
        for e in self.E:
            if not e[0] in self.edge:
                self.edge[e[0]] = []
            self.edge[e[0]].append(e[1])

    
    def DFS(self, v):
        self.visit[v] = True
        self.stack.append(v)
        # if self.funcNm == "putcode":  print(self.stack)

        if not v in self.edge:  # if END
            self.path.append(self.stack.copy())
            self.stack.pop()
            # if self.funcNm == "putcode":  print(self.stack)
            return
        
        for vertex in self.edge[v]: # connected with v
            if not self.visit[vertex]:  # not visited
                self.DFS(vertex)
                self.visit[vertex] = False
            elif not self.loop.get(vertex) == None:
                if self.loop.get(vertex) < self.MAX_LOOP -1:    # visited, but not MAX_LOOP loop
                    self.loop[vertex] += 1
                    self.DFS(vertex)
                    self.loop[vertex] -= 1
 

        # Loop End Path
        loop_count, next_vertex_count = 0, 0
        for next_vertex in self.edge[v]: # connected with v
            next_vertex_count += 1
            if self.loop.get(next_vertex) == self.MAX_LOOP -1:   # MAX_LOOP times visited loop
                loop_count += 1
        if loop_count == next_vertex_count:
            exist_next_next_path = False
            for next_vertex in self.edge[v]: # connected with v
                for next_next_vertex in self.edge[next_vertex]:
                    if not self.loop.get(next_next_vertex):
                        exist_next_next_path = True
            if exist_next_next_path:
                self.DFS(vertex)
                self.visit[vertex] = False   
            else:          
                self.path.append(self.stack.copy())

        self.stack.pop()
        # if self.funcNm == "putcode":  print(self.stack)


    def optimize(self):
        path = []
        for p in self.path:
            for l in self.loop.keys():
                self.loop[l] = p.count(l)
            diff = set(self.loop.values()) - {0,self.MAX_LOOP,self.MAX_LOOP+1}
            if not diff:
                path.append(p)
        self.path = path.copy()

        
    def make_syspath(self):
        syscallpath = []
        for path in self.path:
            for bb in path:
                for v in self.vList:
                    if v.bbNum == bb:
                        syscallpath.extend(v.syscallList.copy())
            
            syscallpath = list(filter(None, syscallpath)) # empty list delete
            if syscallpath not in self.syscallpath:
                self.syscallpath.append(syscallpath.copy())
            syscallpath = []