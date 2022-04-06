'''
standard binary search.
search the target from the given sorted array of numbers, returns the index of the element if found, otherwise returns -1.
'''


def equal_to(array, target):
  
  if type(array) is not list or (type(target) is not int and type(target) is not float):
    raise TypeError('array is not a list, or target is not a number.')
  if len(array) == 0:
    raise ValueError('given list is an empty list.')
    
  low, high = 0, len(array)-1
  
  while(high >= low):

    mid = low + ((high-low)>>1)
    if target == array[mid]:
      return mid

    if target < array[mid]:
      high = mid-1
    else:
      low = mid+1
  
  return -1


'''
binary search for the first equal to the target
search the target from the given sorted array of numbers, returns the index of the element if found, otherwise returns -1.
'''

def first_equal_to(array, target):
  
  if type(array) is not list or (type(target) is not int and type(target) is not float):
    raise TypeError('array is not a list, or target is not a number.')
  if len(array) == 0:
    raise ValueError('given list is an empty list.')
    
  low, high = 0, len(array)-1
  
  while(high >= low):

    mid = low + ((high-low)>>1)

    # removes the numbers greater than the target
    if target < array[mid]:
      high = mid-1
    # removes the numbers little than the target
    elif target > array[mid]:
      low = mid+1
    # keeps the numbers equals to the target, keep shrinking the equals from the higher edge
    # until reaches the left boundary or finds the [mid-1] less than the target.
    else:
      if mid == 0 or array[mid-1] != target:
        return mid
      high = mid-1
  return -1


if __name__ == '__main__':
  
  numbers = [1, 2, 3, 4, 5]
  target = 0
  print(equal_to(numbers,target))



  