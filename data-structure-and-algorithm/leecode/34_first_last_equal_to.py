
'''
Given an array of integers nums sorted in ascending order, find the starting and ending position of a given target value.
Your algorithm's runtime complexity must be in the order of O(log n).
If the target is not found in the array, return [-1, -1] .
'''

def first_last_equal_to(arr, target):
  
  low, high = 0, len(arr)-1
  indices = [-1,-1]

  while high >= low:
    
    mid = low + ((high-low)>>1)
    
    # removes the numbers greater than the target
    if arr[mid] > target:
      high = mid - 1
    # removes the numbers little than the target
    elif arr[mid] < target:
      low = mid + 1
    # keeps the numbers equal to the target
    else:
      if mid == 0 or arr[mid-1] < target:
        indices[0] = mid
        break
      high = mid-1
  
  low, high = 0, len(arr)-1

  while high >= low:

    mid = low + ((high-low) >> 1)

    if arr[mid] > target:
      high = mid - 1
    elif arr[mid] < target:
      low = mid + 1
    else:
      if mid == len(arr)-1 or arr[mid+1] > target:
        indices[1] = mid
        break
      low = mid+1
  return indices

if __name__ == '__main__':
  numbers = [1,2,3,3,3,3,4,5,5,5]
  target = 5
  print(first_last_equal_to(numbers,target))