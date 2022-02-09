import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
# %matplotlib inline

Graph_A = nx.DiGraph()
Graph_B = nx.DiGraph()
Graph_C = nx.DiGraph()
Nodes = range(1,6)
Edges_OK = [(1,2),(1,3),(2,3),(3,1),(3,2),(3,4),(4,5),
            (4,6),(5,4),(5,6),(6,5),(6,1)]
Edges_dead_end = [(1,2),(1,3),(3,1),(3,2),(3,4),(4,5),
                  (4,6),(5,4),(5,6),(6,5),(6,1)]
Edges_trap = [(1,2),(1,3),(2,3),(3,1),(3,2),(3,4),(4,5),
              (4,6),(5,4),(5,6),(6,5)]
Graph_A.add_nodes_from(Nodes)
Graph_A.add_edges_from(Edges_OK)
Graph_B.add_nodes_from(Nodes)
Graph_B.add_edges_from(Edges_dead_end)
Graph_C.add_nodes_from(Nodes)
Graph_C.add_edges_from(Edges_trap)

def initialize_PageRank(graph):
    
    nodes = len(graph)
    
    # M represents the outbound links from row(i) to col(j). shape = (6,6)
    M = nx.to_numpy_matrix(graph)  
    print(f'outbound links from row(i) to col(j):\n{M}')
    
    # outbound counts the total outbound links come from each row. shape= (6,)
    
    outbound = np.ndarray.squeeze(np.asarray(np.sum(M, axis=1)))
    # print(outbound)
  
    
    # probability distribution of outbounds from each node, shape= (6,)
    prob_outbound = np.asarray([1.0/count if count>0 else 0.0 for count in outbound]).reshape(6,1)
    # print(prob_outbound)
    
    # outbound transition matrix, shape= (6,6)
    OutTransMx = np.asarray(np.multiply(M, prob_outbound))
    # print(OutTransMx)
    
    # transpose outbound transition matrix to inbound transition matrix
    InTransMx = OutTransMx.T
    print(f'inbound transition matrix:\n {InTransMx}')
    
    p = np.ones(nodes) / float(nodes)
    
    if np.min(np.sum(OutTransMx,axis=1)) < 1.0:
        print ('Warning: G is substochastic')
    return InTransMx, p



def PageRank_naive(graph, iters = 50):
    inTransMx, p = initialize_PageRank(graph)
    for i in range(iters):
        p = np.dot(inTransMx,p)
    return np.round(p,3)

def PageRank_teleporting(graph, iters = 50, alpha=0.85, rounding=3):
  G, p = initialize_PageRank(graph)
  u = np.ones(len(p)) / float(len(p))
  for i in range(iters):
    p = alpha * np.dot(G,p) + (1.0 - alpha) * u 
  return np.round(p / np.sum(p), rounding)


def test():
  print(f'B: {PageRank_naive(Graph_B)}')
  print(f'C: {PageRank_naive(Graph_C)}')
  
  print(f'A:{PageRank_teleporting(Graph_A, rounding = 10)}')
  print(f'B:{PageRank_teleporting(Graph_B, rounding = 10)}')
  print(f'C:{PageRank_teleporting(Graph_C, rounding = 10)}')

if __name__ == '__main__':
  test()
