'''
  Given n non-negative integers a1, a2, ..., an , where each represents a point at coordinate (i, ai). 
  n vertical lines are drawn such that the two endpoints of line i is at (i, ai) and (i, 0). 
  Find two lines, which together with x-axis forms a container, such that the container contains the most water.
  Note: You may not slant the container and n is at least 2.
'''
from typing import List

class Solution:
  def container_with_most_water(self, arr):
    # validate inputs. 
    if len(arr) < 2:
      raise ValueError('length of input array should has more than 2 elements.')
    for e in arr:
      if e < 0: 
        raise ValueError('elements of the input array should not be a negative number.')

    # initialize the max_water
    max_water = 0
    max_left = 0
    max_right = 0

    # start the outter iteration.
    for left in range(len(arr)-1): 
      for right in range(left+1, len(arr)):
        water = (right-left) * min(arr[left], arr[right])
        if water > max_water:
          max_water = water
          max_left = left
          max_right = right
    return max_water, max_left, max_right

  def container_with_most_water_pointer(self, arr):
    # validate inputs. 
    if len(arr) < 2:
      raise ValueError('length of input array should has more than 2 elements.')
    for e in arr:
      if e < 0: 
        raise ValueError('elements of the input array should not be a negative number.')

    # initialize the max_water
    max_water = 0
    max_left = 0
    max_right = 0
    left, right = 0, len(arr)-1

    while left < right:
      water = (right-left)*min(arr[left], arr[right])
      if water > max_water:
        max_water, max_left, max_right = water, left, right
      if arr[left] < arr[right]:
        left += 1  
      else:
        right -= 1
    
    return max_water, max_left, max_right



if __name__ == '__main__':
  arr = [3,25,25,3,3,3,3,3,3]
  s = Solution()
  r = s.container_with_most_water(arr)
  print(r)

  r = s.container_with_most_water_pointer(arr)
  print(r)
