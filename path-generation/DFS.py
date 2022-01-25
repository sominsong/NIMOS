
from Graph import Graph
from Vertex import Vertex

# Initialization #
vList = [Vertex(1,["print"])]
G = Graph("test",vList)
G.V.extend([0,2,3,4])
G.E.append((2,3))
G.E.append((2,4))
G.E.append((4,2))
G.loop.append(2)
loop_check = dict()

for v in G.loop:
    loop_check[v] = False

print(f"===============Graph Info===============")
print(f"Vertex: {G.V}\nEdge: {G.E}\nLoop: {G.loop}\nLoop Check:{loop_check}")
print(f"========================================\n")


stack = []
visit = dict()
for v in G.V:
    visit[v] = False
path = []

# def find_next(Vfrom, done):
#     print("\nvvvvvvvvvvvvvvvvvvvvv find next vvvvvvvvvvvvvvvvvvvvv")
#     nxt = []
#     for frm, to in G.E:
#         print(f"Vfrom: {Vfrom} | frm: {frm} | to: {to}")
#         if frm == Vfrom:
#             if to in done and not to in G.loop: # loop가 아닌데 이미 방문한 경우, pass
#                 continue
#             if to in G.loop and loop_check[G.loop.index(to)] == True: # loop인데 이미 반복한 경우, pass
#                 continue
#             if to in done and to in G.loop: # loop인데 또 방문하려는 경우, loop check
#                 loop_check[G.loop.index(to)] = True
#                 print(f"loop_check: {loop_check}")         
#             nxt.append(to)
#             print(f"nxt: {nxt}")
    
#     print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
#     return nxt



# def dfs(to, done, path):
#     while to:
#         Vfrom = to.pop()
#         print(f"Vfrom: {Vfrom} | to: {to}")
#         done.append(Vfrom)
#         print(f"done: {done}")
#         path.append(Vfrom)
#         print(f"path: {path}")
#         Vto = find_next(Vfrom, done)
#         print(f"Vto: {Vto}")
#         if Vto: # 다음 방문할 Vertex가 있다면
#             to.extend(Vto)  # to에 Vertex 리스트 추가
#             print(f"to: {to}")
#             dfs(to, done, path)

#         else:   # 마지막 Vertex라면
#             if not to:  # 방문 예정 Vertex가 없다면
#                 print(f"<<<< PATH: {path}>>>>")
#                 G.path.append(path.copy())  # path 등록 후 종료
#                 break
#             else:   # 방문 예정 Vertex가 있다면
#                 print(f"<<<< PATH: {path}>>>>")
#                 G.path.append(path.copy())  # path 등록 후 이전 상태로 되돌리기


def find_next(v, visit):
    nxt = []
    for frm, to in G.E:
        if frm == v:
            if to in G.loop:    # loop 시작점인 경우
                if not visit[to]:   # 방문한 적이 없으면
                    nxt.append(to)
                elif loop_check[to] == False:   # 두 번째 방문일 경우
                    loop_check[to] = True
                    nxt.append[to]
                else:   # 세 번째 이상 방문일 경우
                    break
            else:   # loop가 아닌 경우
                if not visit[to]:   # 방문한 적이 없으면
                    nxt.append(to)

    return nxt


def dfs(V):
    visit[v] = True
    stack.append(v)

    if not find_next(v, visit): # 마지막 노드 일 경우
        path.append(stack) # path 완성
        print(f"path: {stack}")
        stack.pop()
        return

    for frm, to in G.E:
        if not visit[to]:
            dfs(to)
            visit[to]=False

    stack.pop()





#----------------< START >------------------#

dfs(0)