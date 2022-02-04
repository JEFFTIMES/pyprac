from graph_samples import weighted_graph as graph
from priority_queue import PriorityQueue

def prim_mst(graph, start):
  branches = {}
  pq = PriorityQueue()
  total_weight = 0
  pq.push(0,(start, start)) # initialize the priority queue with a zero weight edge (start, start)

  while pq:
    weight, (node_start, node_end) = pq.pop()     # pop up the branch with minimum weight, walk through the branch to the node_end,
    if node_end not in branches:                  # if node_end does not exist in the branches, add the branch in the branches, count the weight.
      branches[node_end]= node_start              # save the newly descovered node, let the node_end as the key, the node_start as the value, 
      total_weight += weight                      # that helps the next time checking.
      for node_next, weight in graph[node_end].items():   # then take the end as the next start node, to check the branches which start with it 
        pq.push(weight, (node_end, node_next))            # push each branch which start from current node_end in the pq with the weight.

  return total_weight, [(start, end) for end, start in branches.items()][1:]

def prim_mst2(graph, start): 
  treepath = {}
  total = 0
  queue = PriorityQueue()
  queue.push(0 , (start, start))    #push the first edge which from start to start, weight=0
  while queue:
    # pop the min weight edge
    weight, (node_start, node_end) = queue.pop()    

    if node_end not in treepath:
      treepath[node_end] = node_start
      if weight:
        print("Added edge from %s to %s weighting %i" % (node_start, node_end, weight)) 
        total += weight
      for next_node, weight in graph[node_end].items():
        queue.push(weight , (node_end, next_node))
  print ("Total spanning tree length: %i" % total)
  return [(start, end) for end, start in treepath.items()][1:]

def test():
  total_weights, tree = prim_mst(graph,'A')
  print(graph)
  print(total_weights, tree)

if __name__ == '__main__':
  test()