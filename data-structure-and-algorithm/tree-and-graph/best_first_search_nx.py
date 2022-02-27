import numpy as np
import networkx as nx
from create_maze import create_maze
'''
calculate and return the euclidean distance between vertex a and vertex b.
'''
def euclidean_dist(a, b, coord):
  (x1, y1) = coord[a]
  (x2, y2) = coord[b]
  return np.sqrt((x1-x2)**2+(y1-y2)**2)

'''
calculate and return the manhattan distance between vertex a and vertex b.
'''
def manhattan_dist(a, b, coord):
  print(a,b, coord)
  (x1, y1) = coord[a]
  (x2, y2) = coord[b]
  return abs(x1 - x2) + abs(y1 - y2)

'''
get the weight attribute of the given edge (a,b).
'''
def graph_weight(graph, a, b):
  return graph.edges[a,b]['weight']

'''
get all the neighbors of the given node.
'''
def node_neighbors(graph, node):
  return [n for n in graph.neighbors(node)]

'''
reconstruct the path from the given connections dict, from the start to the goal.
'''
def reconstruct_path(connections, start, goal):
  if goal in connections:
    current = goal
    path = [current]
    while current != start:
      current = connections[current]
      path.append(current)
    return path[::-1]

'''
calculate the total distance for the given path.
'''
def compute_path_dist(path, graph):
  if path:
    run = 0
    for step in range(len(path)-1):
      A = path[step]
      B = path[step+1]
      run += graph_weight(graph, A, B) 
    return run
  else:
    return 0

'''
Best-first-search
bfs() receives five params: graph, start, goal, and scoring.
the graph is an networkx graph object with the coords attribute on the node and 
the weight attribute on the edge. the start and goal represent the start and end 
vertices, the scoring is the function used to calculate the distance between
two vertices. 

one of the difference between best-first-search(bfs) and depth-first-search(dfs) 
is that bfs not only stores the explored nodes along the discovering, but also
saves the distance from each of the explored node to the goal along with the node. 
with the distances in hand, best-first-search finds out the node with minimum 
distance to the goal as the exploring node instead of always using the last 
node which was pushed in the stack in the depth-first-search. 

another difference the best-first-search different from the depth-first-search
is the open_set, it maintains the non-processed vertices and reduces the node
was processed (either walked or discarded) after each iteration, the explored
adds all the discovered nodes accompany with the distances to the goal in the 
same iteration as well, so the intersection between open_set and explored 
extracts all the discovered but still not have been processed nodes. then the 
sorted() jumps in to help choosing the node with minimum distance to the goal.

'''
def bfs(graph, start, goal, scoring):
  open_set = set(graph.nodes()) 
  explored = {start: scoring(start, goal, {start: graph.nodes[start]['coords'], goal: graph.nodes[goal]['coords']})}  
  parents = {}

  while open_set:
    # intersection represents the discovered but not have been processed nodes.
    candidates = open_set & set(explored.keys())

    if len(candidates) == 0:
      print ("Cannot find a way to the goal %s" % goal)
      break

    distances = [(explored[node], node) for node in candidates]
    dist, mini_dist_node =sorted(distances)[0]
      
    if mini_dist_node == goal:
      print ("Arrived at final vertex %s" % goal)
      print ('Unvisited vertices: %i' % (len(open_set)-1))
      break 
    else:
      print("Processing vertex %s, " % mini_dist_node, end="")
      
    # remove the being processed mini_dist_node from the open_list because it either
    # will be walked (added to parents) or be discarded due to no available exits
    open_set = open_set.difference({mini_dist_node})
    
    neighbors = node_neighbors(graph, mini_dist_node)
    to_be_visited = set(neighbors) - set(explored.keys())
    if len(to_be_visited) == 0:
      print ("found no exit, retracing to %s" % parents[mini_dist_node])
    else:
      print ("discovered %s" % str(to_be_visited))  
      for node in to_be_visited:
        explored[node] = scoring(node, goal, {node: graph.nodes[node]['coords'], goal: graph.nodes[goal]['coords']})
        parents[node] = mini_dist_node
  return parents

def test():
  g, p = create_maze(30,symbols=[i for i in range(30)] ,drawing=True)
  start, goal = '0', '22'
  scoring =  manhattan_dist
  connections = bfs(g, start, goal, scoring)
  path = reconstruct_path(connections, start, goal)
  length = compute_path_dist(path,g)
  print(f'path:{path}\nlength:{length}')

if __name__ == '__main__':
  test()

