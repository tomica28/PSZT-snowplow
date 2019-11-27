import networkx as nx
import random
import collections

def is_edge_in_GoE(edge, goe):
    for i in range(len(goe) - 1):
        if(goe[i] == edge[0] and goe[i + 1] == edge[1]):
            return True
        if(goe[i] == edge[1] and goe[i + 1] == edge[0]):
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

def get_list_of_GoE_with_no_common_edge_with_firstGoE(goe_dict):

    # dictionary and accumulation for output
    out_dict = {}
    acc_edge_list = {}
    if len(goe_dict) == 0:
        return [out_dict, acc_edge_list]

    # get first element
    first_key = list(goe_dict.keys())[0]
    out_dict[first_key] = goe_dict[first_key]
    # put edge list of the first GoE into accumulation edge list
    acc_edge_list = get_all_edges_of_GoE(first_key)

    if len(goe_dict) == 1:
        return [out_dict, acc_edge_list]

    for j in range(1, len(goe_dict)):
        is_exist = False
        for e in acc_edge_list:
            if is_edge_in_GoE(e, list(goe_dict.keys())[j]):
                is_exist = True
                break
        if not is_exist:
            out_dict[list(goe_dict.keys())[j]] = list(goe_dict.values())[j]
            acc_edge_list.extend(get_all_edges_of_GoE(list(goe_dict.keys())[j]))

    return [out_dict, acc_edge_list]

def get_weight_orderd_goe_list(goe_dict):
    max_nodes = len(list(goe_dict.keys())[0])
    weight_orderd_goe_list = list()
    for i in range(max_nodes, 1, -1):
        goe_with_the_same_number_of_nodes = {}
        for key in goe_dict:
            if len(list(key)) == i:
                goe_with_the_same_number_of_nodes[key] = goe_dict[key]

        weight_orderd_goe_list.append(goe_with_the_same_number_of_nodes)

    # sort each dictionary in the list
    for i in range(len(weight_orderd_goe_list)):
        weight_orderd_goe_list[i] = dict(sorted(weight_orderd_goe_list[i].items(), key=lambda kv: kv[1]))

    return weight_orderd_goe_list

def remove_all_existed_edges(acc_edge_list, goe_dict):

    if len(acc_edge_list) == 0:
        return goe_dict

    out_dict = {}
    for j in range(len(goe_dict)):
        is_exist = False
        for e in acc_edge_list:
            if is_edge_in_GoE(e, list(goe_dict.keys())[j]):
                is_exist = True
                break
        if not is_exist:
            out_dict[list(goe_dict.keys())[j]] = list(goe_dict.values())[j]
    return out_dict

def get_final_optimal_path(ordered_dict_list):
    acc_edges_list_final = list()
    optimal_path_dict_final = {}
    for i in range(len(ordered_dict_list)):
        # get dictionary at current stage
        dict = ordered_dict_list[i]

        # remove all GoEs at the one-step-lower level if having any common edge
        # with existing edges of the optimal path
        cleaned_dict = remove_all_existed_edges(acc_edges_list_final, dict)

        # get optimal path and accumulation at this stage
        if len(cleaned_dict) > 0:
            acc_edges_list = list()
            optimal_path_dict = {}
            [optimal_path_dict, acc_edges_list] = get_list_of_GoE_with_no_common_edge_with_firstGoE(cleaned_dict)
            # add optimal path and accumulation of this stage to
            optimal_path_dict_final.update(optimal_path_dict)
            acc_edges_list_final.extend(acc_edges_list)
    return optimal_path_dict_final


#example graph for testing
G = nx.Graph()

nodes = ['A', 'B', 'C', 'D', 'E', 'F']
#edges = [('A', 'B', 1), ('B', 'C', 2), ('C', 'D', 4), ('A', 'C', 3), ('A', 'F', 2), ('D', 'F', 3), ('D', 'E', 2), ('E', 'F', 3)]
edges = [('A', 'B', 5), ('B', 'C', 1), ('C', 'D', 2), ('A', 'C', 2),
         ('A', 'F', 2), ('D', 'F', 2), ('D', 'E', 1), ('E', 'F', 1)]
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
#print(list_of_goe)
# print(len(list_of_goe))

goe_dict = {}
for i in list_of_goe:
    goe_dict[tuple(i)] = (total_weight_of_GoE(i, G), nx.shortest_path_length(G, base, i[0], 'weight'), nx.shortest_path_length(G, i[-1], base, 'weight'))

print(goe_dict)

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

# get weight ordered GoE list
# each element of list is a dictionary (GoE, cost) that has the same number of edges
ordered_dict_list = get_weight_orderd_goe_list(goe_dict)

print(ordered_dict_list)

# build the optimal path
optimal_path_dict_final = get_final_optimal_path(ordered_dict_list)

# print optimal path dictionary raw data
print(optimal_path_dict_final)

# get actual path and calculate total cost
# for key in optimal_path_dict_final:











