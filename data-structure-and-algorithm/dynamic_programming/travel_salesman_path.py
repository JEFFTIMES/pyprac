import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations, combinations
# %matplotlib inline

D = np.array([[0,20,16,25,24],
              [20,0,12,12,27],
              [16,12,0,10,14],
              [25,12,10,0,20],
              [24,27,14,20,0]])

# Graph = nx.Graph()
# Graph.add_nodes_from(range(D.shape[0]))
# for i in range(D.shape[0]):
#     for j in range(D.shape[0]):
#         Graph.add_edge(i,j,weight=D[i,j])
# np.random.seed(2)
# pos=nx.shell_layout(Graph)
# nx.draw(Graph, pos, with_labels=True)
# labels = nx.get_edge_attributes(Graph,'weight')
# nx.draw_networkx_edge_labels(Graph,pos,edge_labels=labels)
# plt.show()

# brute force implementation
def tsp_brute_force(D):
  solutions = list(permutations(range(1, D.shape[0])))
  best = ([], np.sum(D))      # best[0] remembers the path, best[1] remembers the total weights of the path.
  print(best)
  for solution in solutions:
    length = 0
    start = 0
    for next in solution:     
      length += D[start, next]
      start = next
    if best[1] > length:
      best = (solution, length)
  final = (tuple([0]+list(best[0])+[0]),best[1]+D[0][best[0][-1]])
  print(final)

tsp_brute_force(D)

# the purpose of the dynamic programming is to reduce the permutational computations of brute force 
# solution to combinational computations. 
# like any dynamic programming solutions, there is a matrix to represent the growing of sub-problems
# from a smaller problem to the largest problem. here the sub-problems are finding the shortest path 
# for the combinations that contain 2 selected cities to all cities, ended with the given cities as 
# the options.
#     c(0,1), c(0,2), c(0,3), c(0,4), c(0,1,2),         c(0,1,3),         c(0,1,4),         c(0,2,3),        c(0,2,4),         c(0,3,4),         c(0,1,2,3),         c(0,1,2,4),        c(0,1,3,4),        c(0,2,3,4),         c(0,1,2,3,4)
#  1    20                            c(0,2)2 +d(2,1)   c(0,3)3 +d(3,1)   c(0,4)4 +d(4,1)                                                        c(0,2,3)3 +d(3,1)   c(0,2,4)4 +d(4,1)  c(0,3,4)4 +d(4,1)                      c(0,2,3,4)4 + d(4,1), c(0,2,3,4)3 + d(3,1), c(0,2,3,4)2 +d(2,1)
#  1                                                                                                                                             c(0,2,3)2 +d(2,1)   c(0,2,4)2 +d(2,1)  c(0,3,4)3 +d(3,1)                                                           
#  2            16                    c(0,1)1 +d(1,2)                                       c(0,3)3 +d(3,2)  c(0,4)4 +d(4,2)                     c(0,1,3)3 +d(3,2)   c(0,1,4)4 +d(4,2)                     c(0,3,4)4 +d(4,2)   c(0,1,3,4)4 + d(4,2), c(0,1,3,4)3 + d(3,2), c(0,1,3,4)1 +d(1,2)
#  2                                                                                                                                             c(0,1,3)1 +d(1,2)   c(0,1,4)1 +d(1,2)                     c(0,3,4)3 +d(3,2)
#  3                    25                              c(0,1)1 +d(1,3)                     c(0,2)2 +d(2,3)                    c(0,4)4 +d(4,3)   c(0,1,2)2 +d(2,3)                      c(0,1,4)4 +d(4,3)  c(0,2,4)4 +d(4,3)   c(0,1,2,4)4 + d(4,3), c(0,1,2,4)2 + d(2,3), c(0,1,2,4,)1 +d(1,3)
#  3                                                                                                                                             c(0,1,2)1 +d(1,3)                      c(0,1,4)1 +d(1,3)  c(0,2,4)2 +d(2,3)                                                                    
#  4                            24                                         c(0,1)1 +d(1,4)                   c(0,2)4 +d(2,4)   c(0,3)3 +d(3,4)                       c(0,1,2)2 +d(2,4)  c(0,1,3)3 +d(3,4)  c(0,2,3)3 +d(3,4)   c(0,1,2,3)3 + d(3,4), c(0,1,2,3)2 + d(2,4), c(0,1,2,3)1 +d(1,4)
#  4                                                                                                                                                                 c(0,1,2)1 +d(1,4)  c(0,1,3)1 +d(1,4)  c(0,2,3)2 +d(2,4)                                                                     

def tsp_dynamic(D):

  # the virtual matrix, memo is initialized with the shortest path from the starting city 0 to any one other city. 
  # the first part of the key (frozenset([0, city, ...]), city) represents the combination of the cities, 
  # the second part represents the ended city of the combination.
  # the first part of the value (distance, [0, city, ...]) represents the total distance of the path
  # and the second part represents the permutation of the cities, which is the shortest path from 0 to the ended city.
  memo = {(frozenset([0, city]), city) : (distance, [0, city]) for city, distance in enumerate(D[0][1:], start=1)}
  
  cities = D.shape[0]

  # the outer loop gradually enlargers the scope of the problem, from 3 cities to covering all the cities. 
  for subset_size in range(2, cities):
    new_memo = dict()
    comb_subsets = combinations(range(1, cities), subset_size)    # Cn-r: n=the rest of cities except the starting city, r= 
    subsets = [ frozenset(comb) | {0} for comb in comb_subsets ]  # add the starting city back to each of the subset.
    print(f'subsets: {subsets}')
    
    # for each given subset of the cities, take every none-starting city as the extend_to city, 
    # in the memo, explore the shortest paths which take every other city except the extend_to 
    # city as the ended city, then add up the length from the ended city to the extend_to city
    # and append the extend_to city to the sequence as the new path with the extend_to city added.
    for subset in subsets: 
      for extend_to in subset - {0}: # fix the extend_to city
        all_paths = []
        for ended in subset - {0, extend_to}:               # explore the paths from each possible ended city to the extend_to city
          length, path = memo[subset-{extend_to}, ended]    # get the minimum length of from starting to the ended city from the memo
          new_length = length + D[ended][extend_to]         # add up the length of from ended city to extend_to city
          new_path = path + [extend_to]                     # add the extend_to to the path sequence
          all_paths += [(new_length, new_path)]             # collect the (length,path) of every possible ended city extends to the same extend_to 
        
        # after all the possible paths with an extend_to city added is explored, 
        # find the minimum path of those from 0 city to the extend_to city, save it 
        # to the new_memo. it becomes the shortest path from 0 city to the extend_to city
        min_path = min(all_paths, key=lambda path: path[0])
        new_memo[(subset, extend_to)] = min_path
    print(f'new memo:{new_memo}')
    memo = new_memo
  # after the explore finished, get the final path and length from the last item of the memo
  # plus the distance from the last city back to started city
  length, path = memo[(frozenset([i for i in range(cities)]), cities-1)]
  final_length = length + D[cities-1][0]
  final_path = path + [0] 
  print(f'final_path: {final_path}, final_length: {final_length}')

tsp_dynamic(D)