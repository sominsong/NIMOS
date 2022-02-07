""" 

path.py
====================

Thie module is for generating path list
with using control flow graph from collected exploit codes.

Todo:
  * merge main function with user-defined function
"""

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from functools import reduce
import operator
import copy
import json

from tool import Logging
log = Logging.Logging("info")

from cfg import get_exploits
from cfg import make_cfg
from Vertex import Vertex
from Graph import Graph

PERM_OUTPUT_PATH = "/opt/output/perm/"
TEMP_OTUPUT_PATH = "/opt/output/temp/"
SEPARATOR = "="

def make_vertex(backContent, G, bbNum):
    """make vertex with library function call statements and
       add vertex to Graph instance 

    Args:
        backContent(list): content string list after bbNum declaration statement.
        G(class Graph): Graph class instance to which bbNum belongs
        bbNum(int): basic block number
    """

    funcList = []
    for line in backContent:
        if "<bb" in line and not "goto <bb" in line:    
            break;
        if "(" in line and ");" in line:
            funcList.append(line.replace(" ","").replace(";",""))
    
    # make Vertex
    V = Vertex(bbNum, funcList)
    # add Vertex
    G.add_vertex(V)

    log.debug(f"V - func {G.funcNm}\t- bb {bbNum} - {funcList}")


def make_edge(backContent, G):
    """make edge with goto call statements and
       add edge to Graph instance 

    Args:
        backContent(list): content string list after function declaration statement.
        G(class Graph): Graph class instance of function
    """

    for line in backContent:
        if ";;" in line and "succs" in line:
            frm = int(line.split()[1])
            splt1 = line.split().index("{")
            splt2 = line.split().index("}")
            for i in range(splt1+1,splt2):
                to = int(line.split()[i])
                G.add_edge((frm, to))
                log.debug(f"E - func {G.funcNm}\t- ({frm},{to})")
        if ";; Function" in line:
            break


def find_loop(loop_info, G):
    """find loop and vertexs in the loop. 

    Args:
        backContent(list): content string list after function declaration statement.
        G(class Graph): Graph class instance of function
    """

    for v in loop_info.split()[2:]:
        G.add_loop(int(v))


def make_graph(EID):
    """make graph for EID. 

    Args:
        EID(str): exploit code id

    Returns:
        graphList: graph list of EID

    Note:
        * Graph: function (e.g. main function, user-defined functions)
        * Vertex: basic block (include information of library functions)
        * Edge: basic block execution flow order
    """

    # START(0), END(1) vertex
    vList = [Vertex(0,[]), Vertex(1,[])]
    graphList = []
    log.debug(f"V - START vertex - bbnum={vList[0].bbNum}, funcList={vList[0].funcList}")
    log.debug(f"V - END vertex - bbnum={vList[1].bbNum}, funcList={vList[1].funcList}")

    with open(f"{TEMP_OTUPUT_PATH}{EID}.c.012t.cfg", "r") as f:
        content = f.read().splitlines()

    for i, line in enumerate(content):
        
        # find user-defined function name and make graph
        if ";; Function" in line:
            funcNm = line.split()[2]
            graphList.append(Graph(funcNm, vList))
            G = graphList[len(graphList)-1]
            make_edge(content[i+1:], G)

        # find loop
        if ";; Loop" in line and not ";; Loop 0" in line:
            G = graphList[len(graphList)-1]
            find_loop(content[i+3], G)

        # find basic block
        if "<bb" in line and not "goto <bb" in line:
            bbNum = int(line.split()[1].replace(">",""))
            G = graphList[len(graphList)-1]
            make_vertex(content[i+1:], G, bbNum)
    
    log.info(f"made Graph for {EID}.c exploit code")
    log.debug(f"Graph Number: {len(graphList)}")
    for G in graphList:
        log.debug(f"Function Name: {G.funcNm} \n\tVertex: {G.V} \n\tVertex Number: {G.vNum} \n\tEdge: {G.E} \n\tLoop: {G.loop}")

    return graphList


def search_graph(G):
    """search graph with DFS algorithm and
       save found path in graph

    Args:
        G(class Graph): instance of Graph class
    """

    log.info(f"Searching the execution pathes of function {G.funcNm}...")
    G.prepare_DFS()

    print(f"Vertex: {G.V}\nVisit: {G.visit}\nEdge: {G.E}\nLoop:{G.loop}")

    G.DFS(0)
    log.info(f"Finished Searching the execution pathes of function {G.funcNm} - path #: {len(G.path)}")
    log.debug(f"path list: {G.path}")

    log.info(f"making the library function execution pathes of function {G.funcNm}...")
    G.make_libpath()
    log.debug(f"libpath list: {G.libpath}")
    log.info(f"Finished making the library function execution pathes of function {G.funcNm}")


def existInName(line, name):
    for n in name:
        if n == '':
            continue
        nm = n + '('
        if nm in line:
            return n
    return False

def merge(node, idx, cur, origin, result, graph, name):
    res = []
    temp = cur.copy()
    if origin == '':
        for i, x in enumerate(graph[name[node]]):
            cur = temp.copy()
            for j, y in enumerate(x):
                if existInName(y, name):
                    t = cur.copy()
                    for z in result[existInName(y, name)]:
                        cur = t.copy()
                        cur.extend(z)
                        merge(node, (i,j), cur, node, result, graph, name)
                    if i == len(graph[name[node]])-1:
                        return
                    else:
                        cur = []
                        break
                else:
                    cur.append(y)
            res.append(cur)
    else:
        x = graph[name[node]][idx[0]]
        cur = temp.copy()
        for j, y in enumerate(x):
            if j <= idx[1]:
                continue
            if existInName(y, name):
                t = cur.copy()
                for z in result[existInName(y,name)]:
                    cur = t.copy()
                    cur.extend(z)
                    merge(node, (idx[0], j), cur, node, result, graph, name)
                return
            else:
                cur.append(y)
        res.append(cur)

    result[name[node]].extend(res)
                   


def merge_graph(graphList):
    # Neet to do Topology Sort?

    result = {'':[]}
    graph = dict()
    name = ['']
    order = []
    for i, G in enumerate(graphList):
        result[G.funcNm] = []
        graph[G.funcNm] = G.libpath
        name.append(G.funcNm)
        order.append(i+1)

    log.debug(f"result - {result}")
    log.debug(f"graph - {graph}")
    log.debug(f"name - {name}")
    log.debug(f"order - {order}")

    for i in order:
        # if name[i] == "main":
        #     continue    # pass main merging
        log.info(f"Start Merging - {name[i]}")
        merge(i, (0,0), [], '', result, graph, name)
        log.info(f"Finish Merging - {name[i]}")
    for G in graphList:   
        result[G.funcNm] = list(filter(None, result[G.funcNm]))  # delete empty element
        G.newlibpath = result[G.funcNm]
        log.debug(f"{G.funcNm}:\t{G.newlibpath}")

def search_path(EID):
    """search execution path of exploit code(EID)

    Args:
        EID(str): Exploit ID
    """
    
    # make graph for EID
    graphList = make_graph(EID)
    # search graph for EID
    for G in graphList:
        search_graph(G)
    # merge graph into main function
    log.info(f"Merging the execution pathes of EID {EID}...")
    if len(graphList) == 1:
        graphList[0].newlibpath = graphList[0].libpath
    else:
        merge_graph(graphList)
    log.info(f"Finished Merging the execution pathes of EID {EID} - total path #: {len(graphList[-1].newlibpath)}")

    return graphList


def save_path(EID, graphList):
    """save path into json file

    Args:
        path(str): list of Library Path of EID

    Note:
        * Use exploit.json file in output directory
        * Save the result in the same json file in output directory
    """
    path  = []
    found = False
    for G in graphList:
        if G.funcNm == 'main':
            path = G.newlibpath

    log.debug(f"Final 'main' merged path- {path}")
    print(path)

    with open(f'{PERM_OUTPUT_PATH}exploit.json','r') as f:
        jsonList = json.load(f)
        jsonList.pop(-1)

    for exploitJson in jsonList:
        if exploitJson['EID'] == EID:
            found  = True
            exploitJson["path"] = path
            break
    if found == True:
        with open(f'{PERM_OUTPUT_PATH}exploit.json','w') as f:
            jsonStr = json.dumps(jsonList)
            f.write(jsonStr)
            log.info(f"wrote {EID} path on {PERM_OUTPUT_PATH}exploit.json")
    else:
        log.warning(f"There is no {EID} in {PERM_OUTPUT_PATH}exploit.json")
    
if __name__ == "__main__":

    # CFG
    eList = get_exploits()

    ###############
    # eList = [['1397','exploitdb']]
    ###############

    make_cfg(eList)
    
    # Path
    for EID, src in eList:
        # check if exist CFG file for EID
        if not os.path.isfile(f"{TEMP_OTUPUT_PATH}{EID}.c.012t.cfg"):
            log.warning(f"{EID} is not created yet. Maybe compilation problem")
            continue
        graphList = search_path(EID)
        # save_path(EID, graphList)