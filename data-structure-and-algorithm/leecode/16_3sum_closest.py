'''
Given an array nums of n integers and an integer target, 
find three integers in nums such that the sum is closest to target. 
Return the sum of the three integers. 
You may assume that each input would have exactly one solution.

Given array nums = [-1, 2, 1, -4], and target = 1.
The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).
''' 

def three_sum_closest(nums, target):
  if not type(nums) == list:
    raise TypeError('nums must be a list.')
  for n in nums:
    if type(n) is not int and type(n) is not float:
      raise ValueError('elements of nums must be int or float.')
  if len(nums) <=2:
    raise ValueError('nums contains less than 3 numbers.')
  
  sorted_nums = sorted(nums)
  start, end = 0, len(sorted_nums)-1
  diff = float('inf')
  while start != end-1:
    two_sum = sorted_nums[start] + sorted_nums[end]
    for i in range(start+1, end):
      three_sum = (two_sum + sorted_nums[i], start, end, i)
      if three_sum[0] == target: 
        return three_sum
      if abs(three_sum[0] - target) < diff:
        sum, diff = three_sum, abs(three_sum[0] - target)
    if three_sum[0] > target:
      end -=1
    else:
      start +=1
  return sum  


if __name__ == '__main__':

  nums = [-1, 2, 1, -4, 1] # [-4,-1,1,1,2]
  target = 1
  print(three_sum_closest(nums, target))