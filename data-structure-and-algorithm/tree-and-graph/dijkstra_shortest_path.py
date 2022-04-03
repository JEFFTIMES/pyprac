from graph_samples import weighted_graph as graph
from graph_samples import numeric_unweighted_graph as uw_graph
from unweighted_to_weighted import unweighted_to_weighted
from pprint import pprint

def get_lowest_cost_node(nodes, processed):
    lowest_cost = float('inf')
    lowest_cost_node = None
    for node,cost in nodes.items():
        if node not in processed and lowest_cost > cost :
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node

def dijkstra(graph, start, finish=None):
    
    # the costs dict{} remembers the minimum costs from the starting node to each remembered node.
    # the parents dict{} remembers the parent of each node, when the finish node is given, it is 
    # initialized as a key in the parents dict with a None value represents its parent is still not
    # being found. once the parent of the finish node is found, the function returned. when the finish
    # node is not given, the function walks through all the nodes of the graph until there is not any 
    # node is not existed in the processed[].
    
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

    # dijkstra algorithm always takes the node with lowest cost to the statring node 
    # as the beginning to explore the next step until reaches the 'finish' node (when 
    # the 'finish' node is given), or exhausts all the nodes of the graph, so it needs 
    # a costs{} to persist the cost of each discovered node to the starting node.
    # other than the cost{}, a parents{} is crafted to log the segments of the path, 
    # and a processed[] is created to avoid looping. 
    # the two important operations the algorithm need to do are, first exploring neighbor 
    # nodes of the lowest_cost_node, second updating the costs{}, parent{} and processed[].

    # within the outter iteration, lays the inner iteration filling up the cost{} and 
    # the parents{}. it grabs each neighbor node of the current lowest_cost_node, 
    # calculates the cost from the starting node to the neighbor via the lowest_cost_node, 
    # and insert/updates the neighbor node to both the costs{} and the parents{}.
    # when the node in the costs{} being revisited again from other pathes, a condition needed
    # to help the inner iteration to determine wether updates the cost or not by camparing
    # the path of current route with its existed cost. 
    
    lowest_cost_node = start 
    cond = True

    while cond :
        neighbors=graph[lowest_cost_node]
        for node, cost in neighbors.items():
            new_cost = costs[lowest_cost_node] + cost
            try: 
                if new_cost < costs[node]:
                    costs[node] = new_cost
                    parents[node] = lowest_cost_node
            except KeyError:
                costs[node] = new_cost
                parents[node] = lowest_cost_node
        processed.append(lowest_cost_node)
        lowest_cost_node = get_lowest_cost_node(costs, processed)
        
        if finish is None:
            cond = lowest_cost_node is not None
        else:
            cond = parents[finish] is None and lowest_cost_node is not None
    
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

    costs, parents, processed = dijkstra(graph, 'A', 'F')
    pprint(parents)
    all = dict()
    for start in graph:
        costs, parents, processed = dijkstra(graph, start)
        all[start] = parents
    pprint(graph)
    pprint(all)

    all2 = dict()
    w_graph = unweighted_to_weighted(uw_graph)
    pprint(w_graph)
    for start in w_graph.keys():
        costs, parents, processed = dijkstra(w_graph, start)
        all2[start] = parents
        for end in parents.keys():
            path, length = present_path(parents,end)
            print(f'path from {start} to {end}: {path}, length={length}')

if __name__ == '__main__':
    test()