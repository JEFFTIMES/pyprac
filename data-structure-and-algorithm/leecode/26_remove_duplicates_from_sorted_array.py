'''
Given a sorted array nums, remove the duplicates in-place such that each element appear only once and return the new length.
Do not allocate extra space for another array, you must do this by modifying the input array in- place with O(1) extra memory.

Given nums = [0,0,1,1,1,2,2,3,3,4],
Your function should return length = 5, with the first five elements of nums
being modified to 0, 1, 2, 3, and 4 respectively.
'''

def remove_duplicates_from_sorted_array(arr):
  if type(arr) is not list:
    raise TypeError('input is not an array.')
  if len(arr) == 0:
    raise ValueError('empty list.')
  
  sp, lp = 0, 0
  while lp != len(arr):
    if arr[lp] > arr[sp]:
      sp += 1
      if sp != lp:
        t = arr[sp]
        arr[sp] = arr[lp]
        arr[lp] = t
      lp += 1
    else:
      lp += 1
  return sp+1, arr

if __name__ == '__main__':
  
  nums = [0,0,1,1,1,2,2,3,3,4]
  l, arr = remove_duplicates_from_sorted_array(nums)
  print(l, arr)