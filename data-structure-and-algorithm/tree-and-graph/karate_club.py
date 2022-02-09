import networkx as nx
import matplotlib.pyplot as plt
# %matplotlib inline

# triads: http://www.stats.ox.ac.uk/~snijders/Trans_Triads_ha.pdf


graph = nx.karate_club_graph()

# visualizing clusters of a network
# pos=nx.spring_layout(graph)
# nx.draw(graph, pos, with_labels=True)
# plt.show()

# discovering cliques which consists of vertices >=4
cliques = nx.find_cliques(graph)
print(f'{[c for c in cliques if len(c) >=4]}')

# Joining cliques of four and more into communities
communities = nx.community.k_clique_communities(graph, k=4)
communities_list = [list(c) for c in communities]
print ('Found these communities: %s' % communities_list)

# getting all nodes of the found communities
nodes_list = [node for community in communities_list for node in community]

# plot subgraph
subgraph = graph.subgraph(nodes_list)
nx.draw(subgraph, with_labels=True)
plt.show()