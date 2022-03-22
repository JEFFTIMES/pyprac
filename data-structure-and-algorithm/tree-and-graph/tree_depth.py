class Node():
  def __init__(self, value=0, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right
  
# count the max depth of the sub trees while postorder traverse the tree.
def tree_depth(root):
  
  # base case
  if root is None:
    return 0
  
  left_depth = tree_depth(root.left)
  right_depth = tree_depth(root.right)
  
  if left_depth > right_depth:
    return left_depth+1
  else:
    return right_depth+1


# postorder traverse the tree to compare the depth of left with it of the right
# return the max depth of the tree and is_balanced boolean value.
def is_balanced(root):

  #base case
  if root is None:
    return 0, True
  
  l_depth, l_balance = is_balanced(root.left)
  r_depth, r_balance = is_balanced(root.right)

  if l_balance and r_balance:                    # the sub trees are balanced
    if abs(l_depth-r_depth) <= 1:                # current tree is balanced
      if l_depth <= r_depth:                     # add up 1 to the largest depth of the sub trees and return true
        return r_depth+1, True 
      else:
        return l_depth+1, True
    else:                                        # current tree is not balanced
      return max(l_depth, r_depth)+1, False


tree = []
for i in range(0,8):
  tree.append(Node(i))

tree[0].left = tree[1]
tree[0].right = tree[2]
tree[1].left = tree[3]
tree[1].right = tree[4]
#tree[2].left = tree[5]
#tree[2].right = tree[6]
tree[4].left = tree[7]

d = tree_depth(tree[0])
print(d)

d, balanced = is_balanced(tree[0])
print(d, balanced)