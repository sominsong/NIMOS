
class Graph:

    def __init__(self, funcNm):
        self.funcNm = funcNm
        self.V = []
        self.E = [(0,2)]
        self.loop = dict()  # for DFS

    def add_loop(self, v):
        if not v in self.loop:
            self.loop[v] = False


# Initialization #
G = Graph("test_main")
#-----CASE 1------#
# G.V.extend([0,2,3,4,5,6,7,1])
# G.E.append((2,3))
# G.E.append((3,5))
# G.E.append((5,3))
# G.E.append((2,4))
# G.E.append((4,6))
# G.E.append((4,7))
# G.E.append((7,4))
# G.add_loop(3)
# G.add_loop(5)
# G.add_loop(4)
# G.add_loop(7)

#-----CASE 2------#
# G.V.extend([0,2,3,4,5,6])
# G.E.append((2,3))
# G.E.append((2,4))
# G.E.append((3,5))
# G.E.append((5,6))
# G.E.append((5,3))
# G.E.append((6,3))
# G.add_loop(3)
# G.add_loop(5)
# G.add_loop(6)


#-----CASE 3------#
# G.V.extend([0,2,3,4,5,1])
# G.E.append((2,3))
# G.E.append((3,4))
# G.E.append((4,5))
# G.E.append((5,3))
# G.add_loop(3)
# G.add_loop(4)
# G.add_loop(5)

#-----CASE 'fixint'------#
G.V.extend([0,2,3,4,5,1])
G.E.append((2,4))
G.E.append((3,4))
G.E.append((4,3))
G.E.append((4,5))
G.E.append((5,1))
G.add_loop(3)
G.add_loop(4)

print(f"=============== Graph Info ===============")
print(f"Vertex: {G.V}\nEdge: {G.E}\nLoop Check:{G.loop}")
print(f"==========================================\n")


visit = dict()
for v in G.V:
    visit[v] = False
path = []

edge = dict()
for e in G.E:
    if not e[0] in edge:
        edge[e[0]] = []
    edge[e[0]].append(e[1])

print(f"visit: {visit}\npath: {path}\nedge: {edge}")

def dfs(v):
    visit[v] = True
    path.append(v)
    print(path)

    if not v in edge: # if END
        print(f"path: {path}")
        path.pop()
        return

    for vertex in edge[v]:  # edge로 이어져있고
        if not visit[vertex]:  # 방문하지 않았으면
            dfs(vertex)
            visit[vertex] = False
        elif G.loop.get(vertex) == False:   # 방문했는데 loop이고 첫 방문일 경우
            G.loop[vertex] = True
            dfs(vertex)
            G.loop[vertex] = False

    loop_count = 0
    next_count = 0
    for vertex in edge[v]:
        next_count += 1
        if G.loop.get(vertex) == True:  # loop이고 방문했을 경우
            loop_count += 1
    if loop_count == next_count:
        print(f"loop end path:{path}")

    path.pop()

#----------------< START >------------------#

print(f"=============== DFS START ===============")
dfs(0)
print(f"=========================================\n")