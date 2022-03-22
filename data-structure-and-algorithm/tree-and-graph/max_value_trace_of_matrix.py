from calendar import c


matrix = [
  [1,10,9,8,9],
  [12,2,15,13,6],
  [4,7,6,14,12],
  [3,11,16,5,1], 
  [12,9,0,21,7]
]

def shape(matrix):
  return len(matrix), len(matrix[0])

def get_left_node(node, matrix):
  rows, cols = shape(matrix)
  if node[0] < rows-1:
    return (node[0]+1, node[1])
  else:
    return None

def get_right_node(node,matrix):
  rows, cols = shape(matrix)
  if node[1] < cols-1:
    return node[0], node[1]+1

def traverse(node, matrix):
  row, col = node
  yield matrix[row][col]
  l_node = get_left_node(node, matrix)
  r_node = get_right_node(node, matrix)
  if not l_node is None:
    for value in traverse(l_node, matrix):
      yield value
  if not r_node is None:
    for value in traverse(r_node, matrix):
      yield value

def max_sum_branch(root, matrix, total_value=0, max_total=[0]):
  row, col = root
  total_value += matrix[row][col]
  l_node= get_left_node(root, matrix)
  r_node= get_right_node(root, matrix)

  if not l_node is None:
    max_sum_branch(l_node, matrix, total_value, max_total)
  if not r_node is None:
    max_sum_branch(r_node, matrix, total_value, max_total)
  if l_node is None and r_node is None and total_value > max_total[0]: 
    max_total[0] = total_value
  # total_value -= matrix[row][col]   # this line is not necessary, total_value is forgetten when the function call is quited.

def max_sum_branch_with_dp(root, matrix, cache={}, max_total=[0], sub_branch_value=[0]):
  row, col = root
  l_node = get_left_node(root, matrix)
  r_node = get_right_node(root, matrix)
  l_sub_value, r_sub_value = 0, 0
  try:
    sub_branch_value[0] = cache[root]       # if the node has been cached, use the cached node value
    if max_total[0] < sub_branch_value[0]:  # remember the max sub branch value
      max_total[0] = sub_branch_value[0]
  except:                                   # if the node has not been cached, do the routine processing
    if not l_node is None:
      max_sum_branch_with_dp(l_node, matrix, cache, max_total, sub_branch_value)
      l_sub_value = sub_branch_value[0]

    if not r_node is None:
      max_sum_branch_with_dp(r_node, matrix, cache, max_total, sub_branch_value)
      r_sub_value = sub_branch_value[0]

    if l_sub_value > r_sub_value:   # get the maximum sub branch from the left/right pair
      max_sub_value = l_sub_value
    else:
      max_sub_value = r_sub_value

    sub_branch_value[0] = matrix[row][col] + max_sub_value    # save the sub branch value up to this node
    cache[root] = sub_branch_value[0]                         # cache the sub branch value
    if max_total[0] < sub_branch_value[0]:                    # remember the max sub branch value
      max_total[0] = sub_branch_value[0]
  return max_total[0]

def max_weighted_branch(root, matrix, weights, final, path=[]):
  row, col = root
  weights -= matrix[row][col]
  path.append(matrix[row][col])

  l_node= get_left_node(root, matrix)
  r_node= get_right_node(root, matrix)

  if not l_node is None:
    max_weighted_branch(l_node, matrix, weights, final, path)
  if not r_node is None:
    max_weighted_branch(r_node, matrix, weights, final, path)
  if l_node is None and r_node is None and weights == 0:
    final += path[0:] 
  weights += matrix[row][col]
  path.pop()
  



def test():

  m = [0]
  max_sum_branch((0,0), matrix, 0, m)
  print(m[0])

  # f = list()
  # max_weighted_branch((0,0), matrix, m[0], f, [])
  # print(f)

  cache = {}
  ma = max_sum_branch_with_dp((0,0), matrix, cache)
  print(ma, cache)

if __name__ == '__main__':
  test()
