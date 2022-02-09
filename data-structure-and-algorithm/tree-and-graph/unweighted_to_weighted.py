from tkinter import W
from graph_samples import numeric_unweighted_graph as unweighted_graph

def unweighted_to_weighted(uw_graph):
  w_graph = dict()
  for start in uw_graph.keys():
    w_graph[start] = dict()
    for end in uw_graph[start]:
      w_graph[start][end] = 1
  return w_graph

if __name__ == '__main__':
  weighted_graph = unweighted_to_weighted(unweighted_graph)
  print(unweighted_graph,weighted_graph )