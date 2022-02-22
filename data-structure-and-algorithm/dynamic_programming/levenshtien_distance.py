import numpy as np
import pandas as pd
s2 = 'Saturday'
s1 = 'Sunday'
r = len(s1)   # take the s1 as the row of the matrix
c = len(s2)   # take the s2 as the col of the matrix
D = np.zeros((r+1,c+1))  # create the matrix with one more row and one more col to save the initiating values
D[0,:] = list(range(c+1)) 
D[:,0] = list(range(r+1))

# start the compare between the letters of each word
# from the first letter of the row word to each of the letters from the another one.
# if the s1[row]=s2[col], let the D[row][col] = D[row-1][col-1]
# otherwise, D[row][col] = np.min ([ 
#                               D[row-1][col] +1,   # a deletion
#                               D[row][col-1] +1,   # a insertion
#                               D[row-1][col-1] +1  # a substitution
#                              ])
for row in range(1, r+1):
  for col in range(1, c+1):
    if s1[row-1] == s2[col-1]:
      D[row,col] = D[row-1,col-1]
    else:
      D[row,col] = np.min([ D[row-1,col]+1, D[row,col-1]+1, D[row-1,col-1]+1 ])

pd.DataFrame(D,index=list(' '+s1), columns=list(' '+s2))

# check what modifications happend on the word to transform it to the target.
def modifications(distances, word, target):
  r, c = distances.shape
  length_word = len(word)
  length_target = len(target)
  operations = dict()
  actions = []
  if r != length_word+1 or c != length_target+1:
    raise ValueError('length of word or target must be equal to the length-1 of row or column of the distances.')
  col = c-1
  row = r-1
  for step in range(max(length_word,length_target)):
    operations = dict()
    operations[distances[row-1, col]] = (f'delete the letter:{word[row-1]}', (row-1, col))
    operations[distances[row, col-1]] = (f'insert the letter:{target[col-1]}', (row, col-1))
    if word[row-1] == target[col-1]:
      operations[distances[row-1, col-1]] = (f'keep the letter:{word[row-1]}', (row-1, col-1))
    else:
      operations[distances[row-1, col-1]] = (f'substitute the letter:{word[row-1]} with the letter:{target[col-1]}', (row-1, col-1))
    action = min(operations.keys())
    actions += [operations[action][0]]
    row, col = operations[action][1]
  return actions


actions = modifications(D, s1, s2)
print(actions[::-1])