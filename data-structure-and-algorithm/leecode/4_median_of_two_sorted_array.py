'''
There are two sorted arrays nums1 and nums2 of size m and n respectively.
Find the median of the two sorted arrays. 
The overall run time complexity should be O(log (m+n)). You may assume nums1 and nums2 cannot be both empty.
'''

from typing import List, Tuple, Dict, Set
import numpy as np


class Solution:
  def median_of_two_sorted_array(self, arr1: List[int], arr2: List[int]) -> float:
    
    # always takes the shorter array as the first param.
    if len(arr1) > len(arr2):
      return self.median_of_two_sorted_array(arr2, arr1)

    # validate inputs
    if len (arr2) == 0:
      raise ValueError('one of the two arrays should not be empty.')

    # one of the arrays is an empty array.
    if len(arr1) == 0:
      if len(arr2) & 1:
        return arr2[len(arr2)>>1]
      else:
        return  (arr2[len(arr2)>>1] + arr2[(len(arr2)>>1)-1]) /2

    # initiates the start, end, toMedian, m1, m2
    start, end, toMedian, m1, m2 = 0, len(arr1), (len(arr1) + len(arr2) +1) >> 1, 0, 0

    # iterates all the numbers in arr1 to find the proper m1 an m2
    # m1 = the total numbers in arr1 which less than or equal to the median of the concatenated array
    # m2 = the total numbers in arr2 which less than or equal to the median of the concatenated array
    # in the zero based array arr1[] or arr2[], arr1[m1] and arr2[m2] is the first number more than the
    # median of the concatenated array respectively.
    for number in arr1:
      m1 = start + ((end - start) >> 1)
      m2 = toMedian - m1
      # print(f'arr1[m1]:{arr1[m1]},arr2[m2]:{arr2[m2]}')
      # move m1 to a smaller number if arr1[m1-1] >= arr2[m2]
      if m1 > 0 and arr1[m1-1] >= arr2[m2] :
        end = m1 - 1

      # move m1 to a larger number if arr1[m1] <= arr2[m2-1]
      elif m1 < len(arr1) and arr1[m1] <= arr2[m2-1] :
        start = m1 + 1

      # toMedian found
      else:
        break

    # odd total length: median is the large one of arr1[m1-1] and arr2[m2-1]
    if (len(arr1) + len(arr2)) & 1 : 
      # m1 == 0 means none of arr1's number is larger than median, so the median is the arr2[m2-1]
      # m1 == len(arr1) means all the numbers of arr1 are larger than median, so the median is the arr2[m2-1]
      if m1 == 0 or m1 == len(arr1) : 
        return arr2[m2-1]
      return max(arr1[m1-1], arr2[m2-1])
      
    # even total length: median is the larger one in (arr1[m1-1], arr2[m2-1])
    # plus the smaller one in (arr1[m1], arr2[m2]) and divide by 2 
    else:
      # the same as the odd length concatenated array, when m1 == 0 or m1 == len(arr), all the median
      # numbers exist in arr2.
      if m1 == 0 or m1 == len(arr1):
        return (arr2[m2] + arr2[m2-1]) / 2
      return (max(arr1[m1-1], arr2[m2-1]) + min(arr1[m1], arr2[m2])) / 2


if __name__ == '__main__':

  a1, a2 =  [5,6,9,15,25,30,37] , [1,3,8,9]
  print(a1,a2)
  print(sorted(a1+a2), len(a1)+len(a2))
  print(np.median(a1 + a2))
  s = Solution()
  r = s.median_of_two_sorted_array(a1, a2)
  print(r)