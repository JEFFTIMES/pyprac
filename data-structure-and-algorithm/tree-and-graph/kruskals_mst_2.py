from copy import deepcopy
from priority_queue import PriorityQueue

class KruskalsMST():
  
  def __init__(self, graph={}):
    
    self.total_weight = 0
    self.tree = []
    self.connected = dict()
    self.graph = dict()
    self.weighted_edges = dict()
    self.pq_weighted_edges = list()

    if graph:
      if not isinstance(graph, dict):
        raise ValueError("Graph must be a dictionary")
      self.graph = deepcopy(graph)
      
    else:
      raise ValueError('Graph must be not empty dictionary')
    
    self.weighted_edges = self.list_weighted_edges(self.graph)
    self.pq_weighted_edges = self.asc_weighted_edges(self.weighted_edges)
    self.initialize_connected_table()

  ''' 
    list out each branch with its weight from the given graph
  '''
  def list_weighted_edges(self, graph):
    weighted_edges = dict()
    for start in graph.keys():
      for end, weight in graph[start].items():
        if (end, start) not in weighted_edges.keys():
          weighted_edges[(start,end)] = weight
    return weighted_edges

  '''
    asc_weighted_edges(weighted_edges) returns a priority_queue instance filled with all the weighted_edges.
  '''
  def asc_weighted_edges(self, weighted_edges):
    pq = PriorityQueue()
    for edges, weight in weighted_edges.items():
      pq.push(weight, edges)
    return pq

  # initialize the connected table with each vertex connects to a list[] which contains the vertex itself.
  def initialize_connected_table(self):
    for vertex in self.graph:
      self.connected[vertex] = [vertex]
  
  def mst(self):

    # iterating all the branches to an empty queue.
    while self.pq_weighted_edges:
      
      print(self.connected)
      # pop up the least weighted branch
      weight, (start, end) = self.pq_weighted_edges.pop()
      
      # check if the end vertex of the branch exists in the start vertex's connected list,
      # if not, 
      # (1) add the branch in the tree[];
      # (2) append the the connected list of the end vertex to the start vertex's connected list, 
      # that makes the start vertex connect to any vertices which connected with the end vertex;
      # (3) update each vertex which in the connected list of the end vertex, let its connected 
      # list point to the start vertex's connected list, that propagates the connection among all 
      # the vertices which connected with the end vertex and the start vertex.
      # if yes, discard the branch because
      # the linked vertices in the connected list could reach current 'end' vertex again, that means
      # there is a loop should be generated if the 'end' vertex is added to the connected list.
      if end not in self.connected[start]:
        self.tree.append((start, end))
        self.total_weight += weight
        self.connected[start] += self.connected[end][:]
        for vertex in self.connected[end]:
          self.connected[vertex] = self.connected[start]
    return self.total_weight, self.tree


def test():

  graph = {
    'A': {'B':2, 'C':3},
    'B': {'A':2, 'C':2, 'D':2},
    'C': {'A':3, 'B':2, 'D':3, 'E':2},
    'D': {'B':2, 'C':3, 'E':1, 'F':3},
    'E': {'C':2, 'D':1, 'F':1},
    'F': {'D':3, 'E':1}
    }
  
  k_mst = KruskalsMST(graph)
  
  print('\ngiven graph', k_mst.graph)
  print('\nweighted_edges:',k_mst.weighted_edges)
  print('\npq_edges:',[item for item in k_mst.pq_weighted_edges])
  
  tree, total = k_mst.mst()
  
  print('\n(tree, total weight):',(tree,total))

if __name__ == '__main__':
  test()