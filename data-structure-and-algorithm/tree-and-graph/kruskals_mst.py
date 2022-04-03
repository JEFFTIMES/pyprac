from priority_queue import PriorityQueue
from copy import deepcopy, copy 

'''
  Kruskal's algorithm for finding out the minimum spanning tree of a given graph
'''
class KruskalsMST():
  
  def __init__(self, graph={}):
    
    self.total_weight = 0
    self.tree = []

    if graph:
      if not isinstance(graph, dict):
        raise ValueError("Graph must be a dictionary")
      self.graph = deepcopy(graph)
      
    else:
      raise ValueError('Graph must be not empty dictionary')
    
    self.weighted_edges = self.list_weighted_edges(self.graph)
    self.pq_weighted_edges = self.asc_weighted_edges(self.weighted_edges)


  ''' 
    list out each branch with its weight from the given graph
    the tuple represents the branch consists of the (end, start) pair
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

  '''
    given a branch and a list branches[], check if the given branch exists in the branches[]
  '''
  def is_branch_in(self, branch, branches):
    diffs = [(set(branch).difference(set(i))) for i in branches]
    return set() in diffs

  '''
    given a branch and a list of branhes which represented by tuples (end, start), 
    check if a looped path exists when the branch is added to the given branches.
    add a branch to the existed branches ends in 3 possible results, no connected 
    vertex, one connected vertex and 2 connected vertices. so a queue is needed to
    persist the connected vertex/vertices found form the branches, then follow these
    1-2 vertices to search further.
    but only a queue is not enough for the searching, because when the connected 
    vertex(A) is found from the existed branches, the other end of it is drawn out as
    next_connected(B), the branch itself is pushed in the queue as (connect(A), next_connected(B)).
    the next time when it is popped up from the queue to compare with the branches,
    the taken connected vertex points to (B), it will find out a connected branch
    (connected(B), next_connected(A)) and push it in the queue. so these two operations
    make a looping trap.
    an auxiliary visited[] list is used to avoid the trap, when a connected branch is 
    found, it is pushed in the visited[] as well.

  '''
  def find_looped_path(self, added_branch, branches=[]):
    
    # initialize branches[] with non-empty given branches, otherwise initialize it with self.tree
    # initialize the queue with the new added branch,
    # save the end vertex of the new added branch for checking the looping.
    if not branches:
      branches = self.tree
    queue = [added_branch]
    visited = []
    end, start = added_branch
    
    while queue:
      extendTo, connected = queue.pop(0) 
      for branch in branches:
        if (set(branch) & set(connected)) != set(): # none empty intersection found, connected
          # get the other end of the connecting branch
          next_connected = set(branch).difference(set(connected)).pop() 
          # check looping
          if next_connected == end:  # looped
            return True
          # add connected branch to the queue for further searching,
          # add it to the visited list to avoid being revisited.
          if not self.is_branch_in((connected, next_connected), visited) :
            queue.append((connected, next_connected)) 
            visited.append((connected, next_connected))
    # all the consecutive branches have been pushed in the queue exhausted, no loop is found.
    return False

  '''
    given a weighted graph represented by { start_vertex : { end_vertex : weight, ...}, ...},
    return the minimum spanning tree of the graph.

    kruskal algorithm sorts all the edges by the weight, it starts building the tree with
    the minimum weight edge, grows the tree one branch at a time by adding the minimum weight
    edge remaining in the sorted edges. before it adds the edge to the tree, it checks if the
    edge create any loop for the existed tree branches, it does not add the edges creates a 
    loop path to the added tree branch. the MST is created after all the edges are processed.

    '''
  def mst(self):
    # keep taking the least weighted edges from the PriorityQueue,
    # add it to the tree if it does not generate a loop, until the PQ is empty
    while self.pq_weighted_edges:
      weight, edge = self.pq_weighted_edges.pop()
      print(weight, edge)
      if not self.find_looped_path(edge, self.tree):
        self.tree.append(edge)
        self.total_weight += weight
    return self.tree, self.total_weight


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