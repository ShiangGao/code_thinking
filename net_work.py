import numpy as np
import time
from copy import deepcopy
import networkx as nx


def topeInit():
    G = nx.DiGraph()
    hosts = ["h" + str(n) for n in range(100)]  # ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    switches = ["s" + str(n) for n in range(100)]  # ['i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r']  #
    G.add_nodes_from(switches)
    # 只把交换机的节点加到拓扑里，不把终端的节点加到拓扑里，可以解决迪杰斯特拉算法把终端节点也当成中间节点计算路由的问题
    switchToSwitch_num = 10
    hostToSwitch_num = 6
    for i in range(len(switches)):  # 交换机互连
        tem_list = np.random.choice(switches, switchToSwitch_num, replace=False)  # int(math.log(len(switches), 2))
        for j in range(0, len(tem_list)):
            if switches[i] != switches[j]:
                G.add_weighted_edges_from(
                    [(switches[i], switches[j], 1), (switches[j], switches[i], 1)])

    for i in range(len(hosts)):  # 终端与交换机互连
        tem_list = np.random.choice(switches, hostToSwitch_num, replace=False)  # int(math.log(len(switches), 2))
        for j in range(0, len(tem_list)):
            G.add_weighted_edges_from(
                [(hosts[i], switches[j], 1), (switches[j], hosts[i], 1)])
    return G, switches, hosts


# def getNewG(G: nx.DiGraph, source: str, target: str) -> nx.DiGraph:  # 保留当前流的拓扑
#     newG: nx.DiGraph = deepcopy(G)
#     newG.add_nodes_from([source, target])
#     nodes = G.nodes()
#     # print("nodes=", nodes)
#     tem_sw1 = np.random.choice(nodes, 10, replace=False)  # 源节点与交换机互连 int(math.log(len(nodes), 2))
#     # print("终端和交换机连接的数量：", len(tem_sw1))
#     for i in range(len(tem_sw1)):
#         newG.add_weighted_edges_from([(source, tem_sw1[i], 1), (tem_sw1[i], source, 1)])
#     # print("newG.node()=", newG.nodes())
#     # print("newG.edge()=", newG.edges())
#     tem_sw2 = []
#     for i in range(len(tem_sw1)):  # 选择目的节点连接的交换机
#         t = np.random.choice(nodes, 1)[0]
#         while t in tem_sw1:
#             t = np.random.choice(nodes, 1)[0]
#         tem_sw2.append(t)
#     # print("tem_sw2=", tem_sw2)
#     for i in range(len(tem_sw2)):  # 目的节点与交换机互连
#         newG.add_weighted_edges_from([(target, tem_sw2[i], 1), (tem_sw2[i], target, 1)])
#     # print("newG.edge()=", newG.edges())
#     return newG


def getRoutes(newG: nx.DiGraph, n: int, source: str, target: str) -> list:
    newNewG: nx.DiGraph = deepcopy(newG)
    routes = []
    for i in range(n):
        try:
            r = nx.dijkstra_path(newNewG, source, target)
        except:
            print("n is too large")
            break
        else:
            routes.append(r)
            for j in range(1, len(r) - 1):
                newNewG.remove_node(r[j])
                # newNewG.add_weighted_edges_from([(r[j], r[j+1], float('inf')), (r[j+1], r[j], float('inf'))])
    return routes

# if __name__ == '__main__':
#     startTime = time.time()
#     G, _, end = topeInit()
#     print(end[0], end[1])
#     # newG = getNewG(G, end[0], end[1])
#     n = 2
#     routes = getRoutes(G, n, end[0], end[1])
#     print("设定的路由数量：", n, ", 找到的路由数量：", len(routes), ", \n路由有：", routes)
#     n = 8
#     routes = getRoutes(G, n, end[0], end[1])
#     print("设定的路由数量：", n, ", 找到的路由数量：", len(routes), ", \n路由有：", routes)
#     endTime = time.time()
#     print("用时：", (endTime - startTime), " s")
