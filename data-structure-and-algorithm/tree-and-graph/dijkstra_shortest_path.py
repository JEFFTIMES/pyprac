from graph_samples import weighted_graph as graph

def get_lowest_cost_node(nodes, processed):
    lowest_cost = float('inf')
    lowest_cost_node = None
    for node,cost in nodes.items():
        if lowest_cost > cost and node not in processed:
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node

def dijkstra(graph, start, finish):
    # initializing the costs table and the parents table
    infinity = float('inf')
    costs = {
        start:0,
        finish:infinity
    }
    parents = {
        finish:None
    }
    processed = []

    # getting the first lowest cost node next to the start node
    lowest_cost_node = start 
    print(f'costs[]:{costs}, \nparents[]:{parents}, \nprocessed[]:{processed}\n')
    print(f'lowest cost node:{lowest_cost_node}')

    while lowest_cost_node is not None:
        # get the neighbors of the node with the lowest cost to the start
        neighbors=graph[lowest_cost_node]

        print(f'neighbors of {lowest_cost_node}: {neighbors}')

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
                    print(f'{node} in costs[]:{costs}\nnew_cost:{new_cost} < costs[{node}]:{costs[node]}, update costs[{node}]={new_cost} and parents[{node}]={lowest_cost_node}')
                    costs[node] = new_cost
                    parents[node] = lowest_cost_node
                else:
                    print(f'{node} in costs[]:{costs}, but new_cost:{new_cost} >= costs[{node}]:{costs[node]}, no update occurred')
            # else lowest_cost_node's neighbor does not exist in the costs{}, add it to the costs{} and the parents{}
            else :
                print(f'{node} not in costs[]:{costs}')
                costs[node] = new_cost
                parents[node] = lowest_cost_node
                print(f'update costs[{node}]={costs[lowest_cost_node] + cost} and parents[{node}]={lowest_cost_node}')

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

        print(f'costs[]:{costs}, \nparents[]:{parents}, \nprocessed[]:{processed}')
        print(f'\nlowest cost node:{lowest_cost_node}')
    return costs, parents, processed


def present_path(parents, finish):
  path = list()
  start = finish
  while True:
    path.append(start+'->')
    try:
      parent = parents[start]
      start = parent
    except KeyError:
      break
  print(''.join(path).rstrip('->'))
  
def test():
  costs, parents, processed = dijkstra(graph,'A','F')
  print(f'costs[]:{costs},\nparents[]:{parents}, \nprocessed[]:{processed}')
  present_path(parents,'F')
if __name__ == '__main__':
  test()