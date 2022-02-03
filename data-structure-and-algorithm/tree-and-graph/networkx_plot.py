import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
#% matplotlib inline

graph = {
    'A': {'B':2, 'C':3},
    'B': {'A':2, 'C':2, 'D':2},
    'C': {'A':3, 'B':2, 'D':3, 'E':2},
    'D': {'B':2, 'C':3, 'E':1, 'F':3},
    'E': {'C':2, 'D':1, 'F':1},
    'F': {'D':3, 'E':1}
}
Graph = nx.Graph()
for node in graph:
    Graph.add_nodes_from(node)
    for edge, weight in graph[node].items():
        Graph.add_edge(node,edge, weight=weight)
pos = { 'A': [0.00, 0.50], 'B': [0.25, 0.75],
        'C': [0.25, 0.25], 'D': [0.75, 0.75],
        'E': [0.75, 0.25], 'F': [1.00, 0.50]}
labels = nx.get_edge_attributes(Graph,'weight')
nx.draw(Graph, pos, with_labels=True)
nx.draw_networkx_edge_labels(Graph, pos, edge_labels=labels)
nx.draw_networkx(Graph,pos)
plt.show()




