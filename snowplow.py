import networkx as nx
import random

def is_edge_in_GoE(edge, goe):
    for i in range(len(goe) - 1):
        if(goe[i] == edge[0] and goe[i + 1] == edge[1]):
            return True
        if(goe[i] == edge[1] and goe[i + 1 == edge[0]]):
            return True
    return False

def total_weight_of_GoE(goe, graph):
    weight = 0
    for i in range(len(goe) - 1):
        weight += graph.get_edge_data(goe[i], goe[i + 1])['weight']
    return weight

def del_redundancy(list_of_goe):
    newList = []
    for i in list_of_goe:
        reversedI = list.copy(i)
        reversedI.reverse()
        if (reversedI in newList or i in newList):
            continue
        newList.append(i)
    return newList

# get all edges of group of edges - GoE
def get_all_edges_of_GoE(goe):
    edge_list = list()
    for i in range(len(goe) - 1):
        tup = (goe[i], goe[i+1])
        edge_list.append(tup)
    return edge_list

# def get_group_of_GoE_with_no_common_edge(goe_list):
#
#     if len(goe_list) < 2 : return  goe_list
#
#     list_of_goe_group = list();
#     index = 0
#     for i in range(len(goe_list) - 2):
#         edge_list = get_all_edges_of_GoE(goe_list[i])
#         for j in range(i+1, len(goe_list) - 1):
#             is_exist = False
#             for e in edge_list:
#                 if is_edge_in_GoE(e, goe_list[j]):
#                     is_exist = True
#                     break
#             if not is_exist:
#                 list_of_goe_group.append()


#example graph for testing
G = nx.Graph()

nodes = ['A', 'B', 'C', 'D', 'E', 'F']
edges = [('A', 'B', 1), ('B', 'C', 2), ('C', 'D', 4), ('A', 'C', 3), ('A', 'F', 2), ('D', 'F', 3), ('D', 'E', 2), ('E', 'F', 3)]
snowPlow = 6
base = 'A'
G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges)

list_of_goe = []

for i in G.edges:
    list_of_goe.append(list(i))

for i in list_of_goe:
    nb1 = dict(G[i[0]])
    nb2 = dict(G[i[-1]])
    goe_weight = total_weight_of_GoE(i, G)
    for k in nb1.keys():
        if is_edge_in_GoE([i[0], k], i):
            continue
        if(goe_weight + nb1[k]['weight'] <= snowPlow):
            temp = list.copy(i)
            temp.insert(0, k)
            list_of_goe.append(temp)
    for k in nb2.keys():
        if is_edge_in_GoE([i[-1], k], i):
            continue
        if (goe_weight + nb2[k]['weight'] <= snowPlow):
            temp = list.copy(i)
            temp.append(k)
            list_of_goe.append(temp)

list_of_goe = del_redundancy(list_of_goe)
# print(list_of_goe)
# print(len(list_of_goe))

# goe_dict = {}
# for i in list_of_goe:
#     goe_dict[tuple(i)] = (total_weight_of_GoE(i, G), nx.shortest_path_length(G, base, i[0], 'weight'), nx.shortest_path_length(G, i[-1], base, 'weight'))

# print(goe_dict)

# we will create states graph here
# reverse the the list of groups of edges
goe_list = list_of_goe;
goe_list.reverse();
#print(goe_list)

# build dictionary with keys are groups of edges (goe), and values are total costs, include:
# 1. base -> start point +
# 2. the sum of length of edges +
# 3. end point -> base
goe_dict = {};
for goe in goe_list:
    goe_dict[tuple(goe)] = (total_weight_of_GoE(goe, G) + nx.shortest_path_length(G, base, goe[0], 'weight') +
                            nx.shortest_path_length(G, goe[-1], base, 'weight'))

print(goe_dict)

# build the graph by looping all goe_dict dictionary
graph_of_states = nx.Graph()
graph_of_states.add_node(0)

# for state in goe_dict:
#     graph_of_states.add_node(state, weight = goe_dict[state])



#graph_of_states.edges()

print(graph_of_states)






