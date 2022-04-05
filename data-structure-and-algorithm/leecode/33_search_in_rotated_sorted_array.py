'''
Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
(i.e., [0,1,2,4,5,6,7] might become [4,5,6,7,0,1,2] ).
You are given a target value to search. If found in the array return its index, otherwise return -1 .
You may assume no duplicate exists in the array.
Your algorithm's runtime complexity must be in the order of O(log n).
'''

# because the array is a rotated ascending array, so it gives two ascending arrays when broken from the break point.
# when divide the rotated array from the middle index, the break point locates either in the left part or the right part.
# if the break point locates in the left part, the right part must be an ascending array, the left part is still a rotated
# array, and vice versa.
# so add conditions to the basic binary search to adjust the boundary pointers according to the shape 
# of the sub arrays works for the problem. 
def search_in_rotated_sorted(arr, target):

  low, high = 0, len(arr)-1
  
  while high >= low :
    mid = low + ((high-low) >> 1)

    # found and return
    if arr[mid] == target:
      return mid
    
    if arr[mid] > arr[low]:                         # [low] to [mid] is an ascending array.
      if target < arr[mid] and target >= arr[low]:  # target locates in the [low] to [mid-1].
        high = mid-1
      else: 
        low = mid+1                                 # target locates in the [mid+1] to [high], also the break point.
        
    else:                                           # [mid] to [high] is an ascending array.
      if target > arr[mid] and target <= arr[high]:
        low = mid+1
      else:
        high = mid-1
  return -1

if __name__ == '__main__':
  arr, target = [9,10,0,1,2,4,5,7,8], 3
  print(search_in_rotated_sorted(arr, target))