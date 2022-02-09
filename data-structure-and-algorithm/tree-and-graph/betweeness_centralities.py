from dijkstra_shortest_path import *
from graph_samples import weighted_graph as graph
from graph_samples import numeric_unweighted_graph as uw_graph
from unweighted_to_weighted import unweighted_to_weighted

# calculates the betweeness_centrality of each edge for the given graph
# returns a dict with the edge as the key and the betweeness centrality of the edge as the value. 
def betweeness_centralities(graph, undirected=True):
    bc = dict()
    reversed_shortest_pathes_table_start_with = dict()
    
    # initialize the betweeness_centralities counting table
    # edges_betweeness_centralities = { edge: 0 for edge in edges_with_weight(graph).keys() }
    
    # for each vertex of the graph
    # get the reversed_shortest_pathes_table for each vertex and compose the reversed_shortest_pathes_table_start_with table
    for start in graph:
        costs, reversed_shortest_pathes_table, processed = dijkstra(graph, start)
        reversed_shortest_pathes_table_start_with[start] = reversed_shortest_pathes_table
        # print(f'reversed_shortest_pathes_tables: {reversed_shortest_pathes_table_start_with}')


        # for each vertex of the graph, 
        # extracts the shortest pathes from it to every other vertices,
        # represents each of the shortest path with a list of tuples in the format of (start, end)
        for end in graph:
            if end is not start:
                edges = shortest_path_edges_from_start_to_finish(reversed_shortest_pathes_table_start_with[start], end)

                # counts the apprance of each edge in the edges_betweeness_centralities dict
                for edge in edges:
                    try:
                        bc[edge] +=1
                    except KeyError:
                        bc[edge] = 1                    
    if undirected:
        reduced = dict()
        for key, value in bc.items():
            if key not in reduced and key[::-1] not in reduced: # check both (a, b) and (b, a) tuples 
                reduced[key] = value 
        return reduced


# receives 3 parameters
# parents,  dictionary which consists of the shortest pathes from the start vertex to each of the other nodes, 
# start and finish,  the start vertex and the finish vertex of the shortest path which is to be checked out,
# returns a list of tuples of the edges which compose the shortest path, in the sequence of from the start to the finish.
def shortest_path_edges_from_start_to_finish(reversed_shortest_path_table_of_start, finish):
    edges = list()
    edge_end = finish
    while True:
        try:
            edge_start = reversed_shortest_path_table_of_start[edge_end]
            # print((edge_start,edge_end))
            edges.append((edge_start, edge_end))
            edge_end = edge_start
        except KeyError:
            break
    return edges[::-1]

# receives the graph, extracts each of the edge with the weight from the graph
# returns a dict in which the edge (start_vertex, end_vertex) as the key, the weight as the value
def edges_with_weight(graph):
    edges = dict()
    for start_vertex in graph.keys():
        for end_vertex, weight in graph[start_vertex].items():
            edges[(start_vertex, end_vertex)] = weight
    return edges


def test():
  betweeness = betweeness_centralities(graph)
  print(f'betweeness: {betweeness}')
  wg = unweighted_to_weighted(uw_graph)
  b2 = betweeness_centralities(wg)
  print(b2)

if __name__ == '__main__':
  test()