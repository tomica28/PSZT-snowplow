import networkx as nx


def is_edge_in_path(edge, path):
    for i in range(len(path) - 1):
        if(path[i] == edge[0] and path[i+1] == edge[1]):
            return True
        if(path[i] == edge[1] and path[i+1 == edge[0]]):
            return True
    return False
def sumPathWeight(path, graph):
    weight = 0
    for i in range(len(path)-1):
        weight += graph.get_edge_data(path[i], path[i+1])['weight']
    return weight
def delRedundancy(pathList):
    newList = []
    for i in pathList:
        reversedI = list.copy(i)
        reversedI.reverse()
        if (reversedI in newList or i in newList):
            continue
        newList.append(i)
    return newList

#example graph for testing
G = nx.Graph()

nodes = ['A', 'B', 'C', 'D', 'E', 'F']
edges = [('A', 'B', 1), ('B', 'C', 2), ('C', 'D', 4), ('A', 'C', 3), ('A', 'F', 2), ('D', 'F', 3), ('D', 'E', 2), ('E', 'F', 3)]
snowPlow = 6
base = 'A'
G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges)

pathList = []


for i in G.edges:
    pathList.append(list(i))

for i in pathList:
    nb1 = dict(G[i[0]])
    nb2 = dict(G[i[-1]])
    pathWeight = sumPathWeight(i, G)
    for k in nb1.keys():
        if is_edge_in_path([i[0], k], i):
            continue
        if(pathWeight + nb1[k]['weight'] <= snowPlow):
            temp = list.copy(i)
            temp.insert(0, k)
            pathList.append(temp)
    for k in nb2.keys():
        if is_edge_in_path([i[-1], k], i):
            continue
        if (pathWeight + nb2[k]['weight'] <= snowPlow):
            temp = list.copy(i)
            temp.append(k)
            pathList.append(temp)

pathList = delRedundancy(pathList)
print(pathList)
print(len(pathList))

pathDict = {}

for i in pathList:
    pathDict[tuple(i)] = (sumPathWeight(i, G), nx.shortest_path_length(G, base, i[0], 'weight'), nx.shortest_path_length(G, i[-1], base, 'weight'))

print(pathDict)




