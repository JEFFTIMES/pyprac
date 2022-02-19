from functools import reduce
from pprint import pprint

items = { 
  'laptop': { 'value': 2000, 'weight': 3 },
  'guitar': { 'value': 1500, 'weight': 1 },
  'stereo': { 'value': 3000, 'weight': 2 },
  'iphone': { 'value': 2000, 'weight': 1 },
  'diamond': { 'value': 4000,'weight': 0.5},
}

def knapsack( items, capacity ):
  # get the size for the smallest knapsack 
  lightest_item = min(items, key=lambda item: items[item]['weight'])
  unit = items[lightest_item]['weight']
  # create the matrix for the sub-knapsack
  # initialize the cells of matrix to meet the arguments requirements from the reduce().
  matrix = [ [[(None,0,0)] for j in range(int(capacity/unit))] for i in range(len(items)) ]
  
  pprint(f'matrix initialized as: {matrix}')
  
  # create the indices for items
  index = dict()
  indexed_items = dict()
  start = 0
  for key, value in items.items() :
    index[start] = key
    indexed_items[start] = value
    start +=1
  # create the weighted sub-knapsacks
  knapsacks = { j: (j+1)*unit for j in range(int(capacity/unit))}
  
  print(f'knapsacks:{knapsacks}\nindex:{index}\nindexed_items:{indexed_items}\n')

  # fill each cell of the matrix row by row and col by col, 
  # with the following rules
  for i in indexed_items.keys():
    for j in knapsacks.keys():

      print(f'working on matrix[{i}][{j}]: {matrix[i][j]}')

      # start from the first row, fill the knapsack j with i item if weight
      #  of item i < capacity of knapsack j
      if i == 0:
        
        print(f'first row, row[{i}]...')
        
        if indexed_items[i]['weight'] <= knapsacks[j]:
          matrix[i][j] += [(index[i], indexed_items[i]['weight'], indexed_items[i]['value']),]  
          
          
          print(f'{index[i]} weight={indexed_items[i]["weight"]} <= knapsacks[{j}] capacity = {knapsacks[j]}')
          print(f'item[{i}] fills knapsacks[{j}]\nmatrix[{i}][{j}] = {matrix[i][j]} ')

      # for the other rows, first try to fill the knapsack[i][j] with 
      # the current item i if it could be filled. if the current item 
      # could be filled in knapsack[i][j], then check what could be 
      # added in the left over capacity(knapsack[j] - indexed_items[i]['weight'])
      # by searching the knapsack in the previous row which capacity 
      # equal to the left over capacity.
      # at last, compare the value of the new filled cell with the value
      # of the same knapsack in the previous row, keep the larger one.
      else:
        
        print(f'other row, row[{i}]...')
        
        # the current item fits the cell
        if indexed_items[i]['weight'] <= knapsacks[j]:
          candidates = [(index[i], indexed_items[i]['weight'], indexed_items[i]['value']),]
          # calculate the left over capacity
          remained_capacity = knapsacks[j] - indexed_items[i]['weight']

          print(f'{index[i]} weight={indexed_items[i]["weight"]} <= knapsacks[{j}] capacity = {knapsacks[j]}')
          print(f'candidates initialized with: {candidates}')
          print(f'remained_capacity = {remained_capacity}')

          # target the best choice for the remaining capacity
          if remained_capacity > 0 :
            previous_best_knapsack = [index for index, capacity in knapsacks.items() if capacity == remained_capacity][0]
            candidates += matrix[i-1][previous_best_knapsack]

            print(f'remained_capacity > 0, fill it with previous best knapsack...')
            print(f'previous_best_knapsack: matrix[{i-1}][{previous_best_knapsack}] has {matrix[i-1][previous_best_knapsack]}')
            print(f'candidates now updated to: {candidates}')

          current_value = reduce( lambda x,y: (None, 0, x[2]+y[2]),  candidates )[2]
          previous_value = reduce( lambda x,y: (None, 0, x[2]+y[2]), matrix[i-1][j] )[2]
          
          print(f'now candidates has {current_value} total value, compare with matrix[{i-1}][{j}] has {matrix[i-1][j]} with total value {previous_value}.')

          if current_value >= previous_value:
            matrix[i][j] = candidates
          else:
            matrix[i][j] = matrix[i-1][j]
          
          print(f'now matrix[{i}][{j}] has {matrix[i][j]}')
        
        else: 
          matrix[i][j] = matrix[i-1][j]

          print(f'{index[i]} weight={indexed_items[i]["weight"]} > knapsacks[{j}] capacity = {knapsacks[j]}')
          print(f'now matrix[{i}][{j}] has {matrix[i][j]}')
      print(f'\n')
  pprint(matrix)
  print(f'\n')

  
  final = { item: {'value': value, 'weight': weight} for item, weight, value in matrix[-1][-1] if item is not None }
  return final


final= knapsack( items, 5)
print(f'final knapsack: {final}\n')
tw, tv = 0, 0
for properties in final.values():
  tw += properties['weight']
  tv += properties['value']
print(f'total items: {len(final)} \ntotal weight: {tw} \ntotal value: {tv}\n')