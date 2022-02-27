import numpy as np
import string
import networkx as nx
import matplotlib.pyplot as plt

'''
calculate and return the euclidean distance between vertex a and vertex b.
'''
def euclidean_dist(a, b, coord):
  (x1, y1) = coord[a]
  (x2, y2) = coord[b]
  return np.sqrt((x1-x2)**2+(y1-y2)**2)


def shape_2d(length):
  iters = round(np.sqrt(length))
  for i in range(iters, 0, -1):
    if length % i == 0 :
      return (int(max(i,length/i)), int(min(i, length/i)))

'''
create_maze() create a maze consists of m x n vertices, it receives
3 params those are seed, symbols and drawing.
if given, the symbols should be a list of symbol to show up as the
name of the vertices, the length of the symbols must be an even number.
if the symbols is not given, 
'''
def create_maze(seed=3, symbols=None, drawing=True):
    np.random.seed(seed)
    if not symbols:
      letters = [l for l in string.ascii_uppercase[:25]] # A-Y
    else:
      letters = [str(s) for s in symbols]
    
    rows, cols = shape_2d(len(letters))
    checkboard = np.array(letters).reshape((rows,cols)) 

    Graph = nx.Graph()

    # generate the {node:coords} dict for each node 
    spacing = 1.0/min(rows,cols)
    coordinates = [(x*spacing, y*spacing) for x in range(rows) for y in range(cols)]
    print(coordinates)
    positions  = {l:c for l,c in zip(letters, coordinates)}
    print(positions)
    for j, node in enumerate(letters):
        Graph.add_nodes_from([node])
        Graph.nodes[node]['coords'] = coordinates[j]
        # define the sliding window for filtering the neighbors of the visiting node
        x, y = j // cols, j % cols
        w_up = max(0, x-1)
        w_down = min(rows-1, x+1)+1 
        w_left = max(0, y-1)
        w_right = min(cols-1, y+1)+1 
        # flatten the surrounding neighbors along with the visiting node to an 1d array
        neighbors = checkboard[w_up:w_down, w_left:w_right]
        adjacent_nodes = np.ravel(neighbors)
        
        # randomly choose [1-4) exit neighbors to connect with, 4 is the maximum exits if the node is at the corners.
        exits = np.random.choice(adjacent_nodes, size=np.random.randint(1,4), replace=False)
        
        for exit in exits:
            if exit != node:    # if the chosen exit is not the visiting node itself, add the edge.
                # calculate the distance of each pair of nodes which connected by a edge,
                # set the distance as the weight of the edge
                length = int(round(euclidean_dist(node, exit, positions)*10,0))
                Graph.add_edge(node, exit, weight=length)
    
    if drawing:
        nx.draw(Graph, positions, with_labels=True)
        labels = nx.get_edge_attributes(Graph,'weight')
        nx.draw_networkx_edge_labels(Graph, positions, edge_labels=labels)
        plt.show()
    
    return Graph, positions

def test():


  graph, coordinates = create_maze(seed=30, symbols=[i for i in range(28)], )
  print(coordinates)

if __name__ == '__main__':
  test()