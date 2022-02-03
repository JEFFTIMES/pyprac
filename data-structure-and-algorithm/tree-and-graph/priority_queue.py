from heapq import heapify, heappop, heappush

''' 
  PriorityQueue class instantiates a priority queue object for pushing, poping workload with its weight,
  the instance also could be iterated for the items.
'''
class PriorityQueue():
  
  def __init__(self):
    self.queue = list()
    heapify(self.queue)
    self.index = dict()

  def push(self, priority, workload):
    #print(f'p:{priority}\tload:{workload}')
    if workload in self.index:
      self.queue = [ (p, w) for (p, w) in self.queue if w != workload  ]
      heapify(self.queue)
    heappush(self.queue, (priority, workload))
    self.index[workload] = priority
  
  def pop(self):
    if self.queue:
      return heappop(self.queue)
    raise KeyError

  def __contains__(self, workload):
    return workload in self.index

  def __len__(self):
    return len(self.queue)

  def __iter__(self):
    return PQIterator(self.queue)


""" 
  PQIterator class provides priority queue a iterator each time the __iter__() method of priority queue is called.
"""
class PQIterator():
  def __init__(self,queue):
    self.queue = queue
    self.index = 0

  def __next__(self):
    if self.index < len(self.queue):
      item = self.queue[self.index]
      self.index += 1
      return item
    raise StopIteration


'''
  unit test
'''
def main():

  pq = PriorityQueue()

  # push items in
  pq.push(3,(1,2))
  pq.push(2,(2,4))
  arr = [item for item in pq]
  print( arr )

  # push duplicate item in
  pq.push(2,(2,4))
  arr = [item for item in pq]
  print( arr )

  # change weight of workload
  pq.push(1,(2,4))
  arr = [item for item in pq]
  print( arr )

  # pop up item
  pq.pop()
  arr = [item for item in pq]
  print( arr )

  # try to pop up item from empty queue, raise KeyError
  pq.pop()
  pq.pop()
  arr = [item for item in pq]
  print( arr )

if __name__ == '__main__':
  main()