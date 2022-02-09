from tkinter import W
from graph_samples import weighted_graph as graph
from graph_samples import numeric_unweighted_graph as uw_graph
from unweighted_to_weighted import unweighted_to_weighted
from pprint import pprint

def get_lowest_cost_node(nodes, processed):
    lowest_cost = float('inf')
    lowest_cost_node = None
    for node,cost in nodes.items():
        if lowest_cost > cost and node not in processed:
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node

def dijkstra(graph, start, finish=None):
    # initializing the costs table and the parents table
    infinity = float('inf')
    costs = {
        start:0,
        finish:infinity
    }
    if finish is not None:
        parents = {
            finish:None
        }
    else: 
        parents = {}    
    processed = []

    # getting the first lowest cost node next to the start node
    lowest_cost_node = start 
    # print(f'costs[]:{costs}, \nparents[]:{parents}, \nprocessed[]:{processed}\n')
    # print(f'lowest cost node:{lowest_cost_node}')

    while lowest_cost_node is not None:
        # get the neighbors of the node with the lowest cost to the start
        neighbors=graph[lowest_cost_node]

        # print(f'neighbors of {lowest_cost_node}: {neighbors}')

        # checking the neighbors is in the costs{} dictionary
        for node, cost in neighbors.items():
            # if node's neighbor exists in the costs{} dict, calculate the new_cost and 
            # compare it to the costs[node], costs[node] represents the cost from start to the node
            # new_cost = costs[lowest_cost_node] + cost, costs[lowest_cost_node] represents 
            # the cost from start node to the lowest_cost_node, 'cost' represents the cost 
            # from lowest_cost_node to this node.
            new_cost = costs[lowest_cost_node] + cost
            if node in costs: 
                # the cost of the new route is lower than the old one, updates both the costs{} and the parents{} dict
                if new_cost < costs[node]:
                    # print(f'{node} in costs[]:{costs}\nnew_cost:{new_cost} < costs[{node}]:{costs[node]}, update costs[{node}]={new_cost} and parents[{node}]={lowest_cost_node}')
                    costs[node] = new_cost
                    parents[node] = lowest_cost_node
                # else:
                    # print(f'{node} in costs[]:{costs}, but new_cost:{new_cost} >= costs[{node}]:{costs[node]}, no update occurred')
            # else lowest_cost_node's neighbor does not exist in the costs{}, add it to the costs{} and the parents{}
            else :
                # print(f'{node} not in costs[]:{costs}')
                costs[node] = new_cost
                parents[node] = lowest_cost_node
                # print(f'update costs[{node}]={costs[lowest_cost_node] + cost} and parents[{node}]={lowest_cost_node}')

            # try: 
            #     if new_cost < costs[node]:
            #         print(f'{node} in costs[]:{costs}\nnew_cost:{new_cost} < costs[{node}]:{costs[node]}, update costs[{node}]={new_cost} and parents[{node}]={lowest_cost_node}')
            #         costs[node] = new_cost
            #         parents[node] = lowest_cost_node
            #     else:
            #         print(f'{node} in costs[]:{costs}, but new_cost:{new_cost} >= costs[{node}]:{costs[node]}, no update occurred')
            # except KeyError:
            #     print(f'{node} not in costs[]:{costs}')
            #     costs[node] = new_cost
            #     parents[node] = lowest_cost_node
            #     print(f'update costs[{node}]={costs[lowest_cost_node] + cost} and parents[{node}]={lowest_cost_node}')


        # add the node to the processed[]
        processed.append(lowest_cost_node)
        # get the next lowest cost node
        lowest_cost_node = get_lowest_cost_node(costs, processed)

        # print(f'costs[]:{costs}, \nparents[]:{parents}, \nprocessed[]:{processed}')
        # print(f'\nlowest cost node:{lowest_cost_node}')
    return costs, parents, processed



def present_path(parents, finish):
    path = list()
    start = finish
    
    while True:
        path.append(str(start) + '-')
        try:
            parent = parents[start]
            start = parent
        except KeyError:
            break
    present_path = ''.join(path).rstrip('-')[::-1]
    length = len(present_path.split('-')) - 1
    return present_path, length



def test():

    all = dict()
    for start in graph:
        costs, parents, processed = dijkstra(graph, start)
        all[start] = parents
    
    pprint(all)

    all2 = dict()
    w_graph = unweighted_to_weighted(uw_graph)
    for start in w_graph.keys():
        costs, parents, processed = dijkstra(w_graph, start)
        all2[start] = parents
        for end in parents.keys():
            path, length = present_path(parents,end)
            print(f'path from {start} to {end}: {path}, length={length}')

if __name__ == '__main__':
    test()