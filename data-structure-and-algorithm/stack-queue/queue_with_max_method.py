class QueueWithMaxMethod():
  
  def __init__(self):
    self.index = 0
    self.queue = []
    self.max_values = []

  def __len__(self):
    return len(self.queue)

  def _count(self):
    return self.index
  
  def push(self, number):
    if type(number) is not int:
      raise ValueError('input must be a number.')
    # pop the numbers which less than the current given number from the back of the max_values, 
    # and push the number with it's index of what of it in the queue to the max_values.
    # then push it in the queue with the index.
    self.index +=1
    while len(self.max_values) > 0 and number > self.max_values[-1][1] :
      self.max_values.pop()
    self.max_values.append((self.index, number))
    self.queue.append((self.index,number))
    
  def pop(self):
    if len(self.queue) == 0:
      return None
    if self.max_values[0][0] == self.queue[0][0]:
      self.max_values.pop(0)
    return self.queue.pop(0)[1]

  def max(self):
    return self.max_values[0][1]

if __name__ == '__main__':
  a = [1,5,7,2,9,4,3,8,5,4,1,0]
  mq = QueueWithMaxMethod()
  for i in range(len(a)//2):
    mq.push(a[i])
  
  print(mq.max())
  for i in range(len(mq)):
    print(mq.pop())