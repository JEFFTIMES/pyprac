'''
Given an unsorted integer array, find the smallest missing positive integer. 

Note:
Your algorithm should run in O(n) time and uses constant extra space.


Input: [1,2,0]
Output: 3

Input: [3,4,-1,1]
Output: 2

Input: [7,8,9,11,12]
Output: 1

'''

def first_missing_positive(numbers):
  
  if type(numbers) is not list:
    raise TypeError('numbers is not a list.')
  if len(numbers) == 0:
    raise ValueError('number is an empty list.')

  map = dict()
  for number in numbers:
    map[number] = number
  
  i = 1
  while True:
    try:
      t = map[i]
    except KeyError:
      return i
    i += 1

if __name__ == '__main__':

  numbers1, numbers2, numbers3 = [7,8,9,11,12], [3,4,-1,1], [1,2,0]
  
  print(first_missing_positive(numbers1))
  print(first_missing_positive(numbers2))
  print(first_missing_positive(numbers3))