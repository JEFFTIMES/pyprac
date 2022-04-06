

def last_lte(array, target):
  
  if type(array) is not list or (type(target) is not int and type(target) is not float):
    raise TypeError('array is not a list, or target is not a number.')
  if len(array) == 0:
    raise ValueError('given list is an empty list.')

  low, high = 0, len(array)-1
  while(high >= low):
    mid = low + ((high-low)>>1)
    # removes the numbers greater than the target.
    if array[mid] > target:                   
      high = mid-1
    
    # shrink from the lower edge until reach right boundary or [mid+1] > target
    else:
      if mid == len(array)-1 or array[mid+1] > target:   
        return mid
      low = mid+1
  return -1


if __name__ == '__main__':
  
  numbers = [1, 2, 3, 4, 5, 9, 10]
  target = 5
  print(last_lte(numbers,target))