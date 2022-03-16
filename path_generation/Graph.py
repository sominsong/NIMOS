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
            self.loop[v] = False
    
    def print_member(self, who, v):
        if not self.funcNm == "do_child":
            return
        if who == "all":
            print(v," - ", "funcNm: ", self.funcNm)
            print(v," - ", "V: ", self.V)
            print(v," - ", "E: ", self.E)
            print(v," - ", "vList: ", self.vList)
            print(v," - ", "vNum: ", self.vNum)
            print(v," - ", "loop: ", self.loop)
            print(v," - ", "visit: ", self.visit)
            print(v," - ", "edge: ", self.edge)
            print(v," - ", "stack: ", self.stack)
            print(v," - ", "path: ", self.path)
            print(v," - ", "syscallpath: ", self.syscallpath)
            print(v," - ", "newsyspath: ", self.newsyspath)
        if who == "V":
            print(v," - ", "V: ", self.V)
        if who == "E":
            print(v," - ", "E: ", self.E)
        if who == "loop":
            print(v," - ", "loop: ", self.loop)
        if who == "visit":
            print(v," - ", "visit: ", self.visit)
        if who == "edge":
            print(v," - ", "edge: ", self.edge)
        if who == "stack":
            print(v," - ", "stack: ", self.stack)
        if who == "path":
            print(v," - ", "path: ", self.path)
        if who == "syscallpath":
            print(v," - ", "syscallpath: ", self.syscallpath)
        if who == "newsyspath":
            print(v," - ", "newsyspath: ", self.newsyspath)
 
    def prepare_DFS(self):
        # make edge dictionary {e: [connected edge list], ...}
        for e in self.E:
            if not e[0] in self.edge:
                self.edge[e[0]] = []
            self.edge[e[0]].append(e[1])

    
    def DFS(self, v):
        self.visit[v] = True
        self.stack.append(v)
        self.print_member("stack", v)

        if not v in self.edge:  # if END
            self.path.append(self.stack.copy())
            self.stack.pop()
            return
        
        for vertex in self.edge[v]: # connected with v
            if not self.visit[vertex]:  # not visited
                self.DFS(vertex)
                self.visit[vertex] = False
            elif self.loop.get(vertex) == False:    # visited, but first loop
                self.loop[vertex] = True
                self.DFS(vertex)
                self.loop[vertex] = False

        # Loop End Path
        loop_count, next_vertex_count = 0, 0
        for vertex in self.edge[v]: # connected with v
            next_vertex_count += 1
            if self.loop.get(vertex) == True:   # twice visited loop
                loop_count += 1
        if loop_count == next_vertex_count:
            self.path.append(self.stack.copy())

        self.stack.pop()
        

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