# given an array of numbers and a size of the sliding window
# find out all the max values when the sliding window get through the array.

# here is the brute force solution, returns the max(window[]) each time the window slides forward.
class MaxSlidingWindow():
  def __init__(self, size):
    self.size = size
    self.dq = []

  def slide(self, number):
    
    if len(self.dq) < self.size:
      self.dq.append(number)
      return None
    else:
      _max = max(self.dq)
      self.dq.pop(0)
      self.dq.append(number)
      return _max

# here is the solution leverages the double end queue.
# each time when the window is fed with a number, it compares the numbers from the end of the dq with it
# and removes those smaller than it, after that it appends the input number at the end of the dq.
# this operation keeps pushing the largest number the window has met at the head of the dq.
# along with the number been passed in is the index of the number, the window compares the comming index
# with that of the head number from the dq to determine pop up the head number or not.
# this operation performs what the sliding window does. 
# the window returns the number at the head position of the dq every time it slides forward, it is the max
# values in the current window.       
class MaxValueSlidingWindow():
  def __init__(self,size):
    self.size = size
    self.dq = [(-1, float('-inf'))]
    self.start = 0
  def slide(self, element):
    if element[0] - self.dq[0][0] >= self.size:
      self.dq.pop(0)
    while len(self.dq) > 0 and element[1] > self.dq[-1][1]:
      self.dq.pop()
    self.dq.append(element)
    return self.dq[0][1]

    
def max_values(numbers, win_size): 
  _max = []
  queue = []
  queue.append((0, numbers[0]))
  for i,v in enumerate(numbers, start=1):
    if i - queue[0][0] >= win_size: 
      queue.pop(0)          # window slides out the left number, pop it out
    while len(queue) > 0 and v > queue[-1][1] :  
      queue.pop()           # remove the elements which smaller than the input from the end of the queue,
    queue.append((i,v))     # then tail the input number at the end
    if i >= win_size:
      _max.append(queue[0][1])  # save the head element to the _max list.
  return _max



if __name__ == '__main__':
  numbers, win_size = [2,4,6,3,1,5,9,8,7,0], 3

  n = numbers + [None]
  r = []
  print(n)
  win = MaxSlidingWindow(win_size)
  for v in n:
    popped = win.slide(v)
    if popped is not None:
      r.append(popped)
  print(r)

  m = max_values(numbers, win_size)
  print(m)

  win2 = MaxValueSlidingWindow(win_size)
  rr = []
  for i,v in enumerate(numbers+[float('-inf')]*(win_size-1)):
    _max = win2.slide((i,v))
    if not _max is None:
      rr.append(_max)
  print(rr)