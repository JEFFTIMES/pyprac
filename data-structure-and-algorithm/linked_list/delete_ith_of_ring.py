class Node():
  index = 0
  def __init__(self,value, next=None):
    self.index = Node.index
    self.value = value
    self.next = next
    Node.index +=1

def create_ring(n):
  
  for i in range(n-1, -1, -1):
    if i == n-1:
      pre_node = Node(i)
      last_node = pre_node
    else:
      node = Node(i, pre_node)
      pre_node = node
  last_node.next = node
  return node

def traverse_circle(node):
  values = [node.value]
  index = node.index
  node = node.next
  while index != node.index:
    values += [node.value]
    node = node.next
  return values


def delete_ith_node(start, i):
  # move to the node after the ith node, and set the next of the node before the ith to it
  # set the start to the node after the ith.
  break_point = start
  next_point = start
  for j in range(i):
    if j < i-2:
      break_point = break_point.next
    next_point = next_point.next
  break_point.next = next_point
  return next_point


def delete_ith_node_with_queue(n,i):
  queue = [e for e in range(n)]
  while len(queue) >= i:
    queue = queue[i:] + queue[0:i-1]
  while len(queue) != 1:
    queue.pop(i-len(queue)-1)
  return queue

if __name__ == '__main__':
  start = create_ring(120)
  remained = []
  while len(remained) != 1:
    remained = traverse_circle(start)
    print(remained)
    start = delete_ith_node(start, 4)

  print(delete_ith_node_with_queue(120,4))

