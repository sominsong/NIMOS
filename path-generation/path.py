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

from tool import Logging
log = Logging.Logging("info")

from cfg import get_exploits
from cfg import make_cfg
from Vertex import Vertex
from Graph import Graph

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


def find_loop(backContent, G):
    """find loop and vertexs in the loop. 

    Args:
        backContent(list): content string list after function declaration statement.
        G(class Graph): Graph class instance of function
    """

    for line in backContent:
        if ";;  header" in line:
            start, end = line.split()[2], line.split()[4]
            G.add_loop(start, end)


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
            find_loop(content[i+1:], G)

        # find basic block
        if "<bb" in line and not "goto <bb" in line:
            bbNum = int(line.split()[1].replace(">",""))
            G = graphList[len(graphList)-1]
            make_vertex(content[i+1:], G, bbNum)
    
    log.info(f"made Graph for {EID}.c exploit code")
    log.debug(f"Graph Number: {len(graphList)}")
    for G in graphList:
        log.debug(f"Function Name: {G.funcNm} \n\tVertex: {G.V} \n\tVertex Number: {G.vNum} \n\tEdge: {G.E}")

    return graphList


def search_graph(G):
    """search graph with DFS algorithm and
       save found path in graph

    Args:
        G(class Graph): instance of Graph class
    """

    log.info(f"Searching the execution pathes of function {G.funcNm}...")
    G.DFS()
    log.info(f"Finished Searching the execution pathes of function {G.funcNm}")
    log.info(f"path list: {G.path}")


def search_path(EID):
    """search execution path of exploit code(EID)

    Args:
        EID(str): Exploit ID
    """
    
    path = []
    # make graph for EID
    graphList = make_graph(EID)
    # search graph for EID
    for G in graphList:
        search_graph(G)

def save_path(EID):
    """save path into json file

    Args:
        path(str): list of Library Path of EID

    Note:
        * Use exploit.json file in output directory
        * Save the result in the same json file in output directory
    """

    # with open(f'{PERM_OUTPUT_PATH}exploit.json','r') as f:
    #     jsonList = json.load(f)
    #     jsonList.pop(-1)
    # with open(f'{PERM_OUTPUT_PATH}exploit.json','w') as f:
    #     for exploitJson in jsonList:
    #         exploitJson["path"] = find_path(EID)
    #     jsonStr = json.dumps(jsonList)
    #     f.write(jsonStr)

if __name__ == "__main__":

    # CFG
    eList = get_exploits()
    ############## [START]DEBUG #################
    eList = [('test','exploitdb'), ('2004','exploitdb'), ('718','exploitdb'), ('2006','exploitdb'),]  
    ############## [END]DEBUG ###################
    make_cfg(eList)
    
    # Path
    for EID, src in eList:
        search_path(EID)
        save_path(EID)