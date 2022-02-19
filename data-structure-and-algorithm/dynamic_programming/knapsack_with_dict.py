from functools import reduce
from pprint import pprint

products = { 
  'laptop': { 'value': 2000, 'weight': 3 },
  'guitar': { 'value': 1500, 'weight': 1 },
  'stereo': { 'value': 3000, 'weight': 2 },
  'iphone': { 'value': 2000, 'weight': 1 },
  'diamond': { 'value': 4000,'weight': 0.5},
}

"""
  redesign the knapsack(), using a dict {(row,col):([item,...],total_value,total_weight)} 
  replace the 2d matrix to cache the choices for each sub-knapsack.
  the row in the tuple of the key refer to the index of the items, and the col refer to the
  capacity of each sub-knapsack. the value consists of a tuple with items in the sub-knapsack,
  the total_value and the total_weight
"""

def knapsack( items, capacity):
  # create the corresponding weights list, values list and the indexed_items dict.
  indexed_items = dict()
  weights = []
  values = []
  i=0
  for name, product in items.items():
    weights += [product['weight']]
    values += [product['value']]
    indexed_items[i] = name
    i += 1
  print(weights, values, indexed_items)

  # get the minimum weight of products, take it as the unit to initialize the capacities of sub-knapsacks 
  unit = min(weights)
  capacities = [(i)*unit for i in range(int(capacity//unit) + 1 )]
  print(capacities)

  # with the indexed_items dict and the capacities list in hand,
  # it's time to initialize the knapsacks dict(), take tuple (-1, capacity) 
  # as the key, tuple ([], 0, 0) to index the naive row.
  knapsacks = {(-1, capacity) : ([], 0.0, 0.0,) for capacity in capacities }
  print(knapsacks)

  # now it's time to find the optimize solution for each of the sub-knapsack item by item.
  # to determine what should be put in the current sub-knapsack indicated by (indexed_items.key, capacities[j])
  # follows the rules of fitting the larger total value items of the current item + left over capacity optimize 
  # solution compare with the solution in the same capacity col of the previous item row.
  for item in indexed_items.keys(): # iterate the items
    for capacity in capacities: # iterate the sub-knapsacks
      # check if item fits the capacity
      if weights[item] <= capacity:
        takes = ([item,], values[item], weights[item])
        remained_capacity = capacity - weights[item]
        rest = knapsacks[(item-1, remained_capacity)]
        knapsacks[(item, capacity)] = (takes[0] + rest[0], takes[1] + rest[1], takes[2] + rest[2]) 
      else: 
        knapsacks[(item, capacity)] = knapsacks[(item-1, capacity)]
  solution = knapsacks[(max(indexed_items.keys()), capacity)]
  print(solution)
  choices = { indexed_items[i]:items[indexed_items[i]] for i in solution[0] }
  ttl_value = solution[1]
  total_weight = solution[2]
  return choices, ttl_value, total_weight

s = knapsack(products, 5.0)
print(s)