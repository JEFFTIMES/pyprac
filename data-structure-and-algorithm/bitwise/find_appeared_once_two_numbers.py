# there is a numerical list in which two numbers appear only once, the other numbers all appear twice.
# find out those two numbers which appear once.

def two_numbers_appear_once(array):
  xor = array[0]
  for i in range(1, len(array)): # xor each element of the array to get rid of all the duplicate numbers
    xor = xor ^ array[i]
  print('xor:{}'.format(xor))
  
  mask = 1
  while not xor&1:      # get the first none zero bit position of the xor result
    mask = mask << 1
    xor = xor >> 1
  print('mask:{}'.format(mask))

  a1, a2 = [], []
  for e in array:       # divide the array by result of the the element & mask 
    if e & mask:
      a1.append(e)
    else:
      a2.append(e)
  print(f'divided:{a1},{a2}')

  n1 = a1[0]
  n2 = a2[0]

  for i in range(1,len(a1)):
    n1 = n1 ^ a1[i]

  for i in range(1, len(a2)):
    n2 = n2 ^ a2[i]
  
  print(f'two numbers appeared once are:{n1},{n2}')

a = [11,22,33,11,2,5,33,22]
print(a)
two_numbers_appear_once(a)