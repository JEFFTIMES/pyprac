'''
Given an array nums and a value val, remove all instances of that value in-place and return the new length.
Do not allocate extra space for another array, you must do this by modifying the input array in- place with O(1) extra memory.
The order of elements can be changed. It doesn't matter what you leave beyond the new length.
'''

# move the finder to find the target number, move last to the index of the number equals 
# to the target when it is found.
# move the finder in the rest elements of the array to find the first number does not equal
# to the target, then swaps it with the number equals to the target represented by the 
# last pointer, and set the finder back to the last.
def remove_element(arr, target):
  finder, last = 0, 0
  while finder != len(arr):
    if arr[finder] == target:
      last = finder
      for finder in range(last+1, len(arr)):
        if arr[finder] != target:
          arr[last], arr[finder] = arr[finder], arr[last]
          finder = last
          break
    # move the finder one step ahead
    finder += 1
  return last, arr

if __name__ == '__main__':
  nums, target = [0,1,2,2,3,0,4,2,2,2], 2
  l, arr = remove_element(nums, target)
  print(l,arr)