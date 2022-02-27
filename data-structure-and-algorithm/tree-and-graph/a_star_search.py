from best_first_search_nx import manhattan_dist, node_neighbors, graph_weight, reconstruct_path, compute_path_dist
from create_maze import create_maze

def astar(graph, start, goal, scoring):
  open_set = set(graph.nodes())
  explored = {start: manhattan_dist(start, goal,{start: graph.nodes[start]['coords'], goal: graph.nodes[goal]['coords']})}
  costs = {start: 0}
  parents = {}
  while open_set:
    candidates = open_set & set(explored.keys())
    if len(candidates)==0:
      print ("Cannot find a way to the goal %s" % goal)
      break
    frontier = [(explored[node], node) for node in candidates]
    dist, min_dist_node =sorted(frontier)[0]
    if min_dist_node == goal:
      print ("Arrived at final vertex %s" % goal)
      print ('Unexplored vertices: %i' % (len(open_set)-1))
      break
    else:
      print("Processing vertex %s, " % min_dist_node, end="")
    
    open_set = open_set.difference({min_dist_node})
    current_weight = costs[min_dist_node]
    neighbors = node_neighbors(graph, min_dist_node)
    to_be_visited = list(set(neighbors)-set(costs.keys()))
    print(f'neighbors: {neighbors}, to_be_visited:{to_be_visited}')
    for node in neighbors:
      new_weight = current_weight + graph_weight(graph, min_dist_node, node)
      if node not in costs or new_weight < costs[node]:
        costs[node] = new_weight
        # the distance value related to the vertex key which stores in the explored dict equals to the 
        # estimation from current node to goal plus the really walked distance from start to current node.
        explored[node] = manhattan_dist(node, goal, {node:graph.nodes[node]['coords'], goal: graph.nodes[goal]['coords']}) + new_weight 
        parents[node] = min_dist_node
    if to_be_visited:
      print ("discovered %s" % to_be_visited)
    else:
      print ("getting back to open set")
  return parents

def test():
  g, p = create_maze(30, symbols=[i for i in range(30)] ,drawing=True)
  start, goal = '0', '29'
  scoring =  manhattan_dist
  connections = astar(g, start, goal, scoring)
  path = reconstruct_path(connections, start, goal)
  length = compute_path_dist(path,g)
  print(f'path:{path}\nlength:{length}')

if __name__ == '__main__':
  test()


