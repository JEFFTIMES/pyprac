from priority_queue import PriorityQueue
from copy import deepcopy, copy 

'''
  Kruskal's algorithm for finding out the minimum spanning the of given graph
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
    given an added_branch, it finds out which end/ends connect to the given branches[], returns a set() which consists of vertices
  '''
  def find_connected_ends(self, added_branch, branches):
    print(f'branches: {branches}')
    set_added_branch = set(added_branch)
    print(f'set({added_branch}): {set_added_branch}')
    connected_nodes = set()
    for branch in branches:
      connected = set(branch) & set_added_branch
      # print(f'set(branch): {set(branch)}, set(added): {set_added_branch}, intersection: {connected}')
      connected_nodes = connected_nodes.union(connected)
    return connected_nodes


  '''
    given a branch and a list branches[], check if the given branch exists in the branches[]
  '''
  def is_branch_in(self, branch, branches):
    diffs = [(set(branch).difference(set(i))) for i in branches]
    return set() in diffs

  '''
    given a branch represented by a tuple (start, connected), check if a looped path exists when the branch is added to the given branches.
  '''
  def find_looped_path(self, added_branch, branches=[]):
    
    # initialize branches[] with non-empty given branches, otherwise initialize it with self.tree
    if not branches:
      branches = self.tree
    # initialize the queue, visited, and the start_end s.
    queue = [added_branch]
    visited = []
    s, e = added_branch
    while queue:
      # print(f'queue:{queue}')
      # pop up the nodes of the first branch from the queue   
      start, connected = queue.pop(0) 
      # print(f'pop up branch to be checked: ({repr(start)},{repr(connected)})')
      for branch in branches:
        # check each branch in the branches[] if it connected to the given branch at the connected vertex
        intersect = set(branch) & set(connected)
        # print(f'branch from branches:{branch} \tset({branch}) & set({connected}) = { intersect }')
        
        if intersect != set(): # connected
          next_connected = set(branch).difference(set(connected)).pop() # get the other end of the iterating branch  
          # if the other end equal to the start end of the added branch, there is a loop
          if next_connected == s:  # looped
            return True
          # otherwise, check if the branch is visited before, if not, add it in the queue for the further searching,
          # and remember it in the visited[] for avoding being reinserted.
          if not self.is_branch_in((connected, next_connected), visited) :
            # print(f'connected branch found:({connected, next_connected})') 
            # when insert the branch in queue, always format the branch 
            # with the other vertex at the end of the tuple.
            queue.append((connected, next_connected)) 
            visited.append((connected, next_connected))
            # print(f'visited:{visited}\n')
    # the queue is exhausted, no loop was found.
    return False

  '''
    given a weighted graph represented by { start_vertex : { end_vertex : weight, ...}, ...},
    return the minimum spanning tree of the graph.
  '''
  def mst(self):
    # keep taking the least weighted edges from the queue, add it to the tree if it does not generate a loop, until the queue is empty
    while self.pq_weighted_edges:
      weight, edge = self.pq_weighted_edges.pop()
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