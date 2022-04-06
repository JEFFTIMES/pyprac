'''
binary search for the last equal to the target
search the target from the given sorted array of numbers, returns the index of the element if found, otherwise returns -1.
'''


def last_equal_to(array, target):
  
  if type(array) is not list or (type(target) is not int and type(target) is not float):
    raise TypeError('array is not a list, or target is not a number.')
  if len(array) == 0:
    raise ValueError('given list is an empty list.')

  low, high = 0, len(array)-1
  
  while(high >= low):

    mid = low + ((high-low)>>1)
    # removes the numbers greater than the target.
    if target < array[mid]:
      high = mid-1
    # removes the numbers less than the target.
    elif target > array[mid]:
      low = mid+1
    # keeps the numbers equal to the target, keeps shrinking the
    # array from the left edge until reach the right boundary or finds [mid+1] > target.
    else:
      if mid == len(array)-1 or array[mid+1] != target:
        return mid
      low = mid+1
  return -1


if __name__ == '__main__':
  
  numbers = [1, 2, 3,3,3,3, 4, 5,5,5]
  target = 1
  print(last_equal_to(numbers,target))