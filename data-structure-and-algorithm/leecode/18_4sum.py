'''
Given an array nums of n integers and an integer target, 
are there elements a, b, c, and d in nums such that a + b + c + d = target? 
Find all unique quadruplets in the array which gives the sum of target.
Note:
The solution set must not contain duplicate quadruplets. 
Example:
Given array nums = [1, 0, -1, 0, -2, 2], and target = 0.
A solution set is:
[
  [-1,  0, 0, 1],
  [-2, -1, 1, 2],
  [-2,  0, 0, 2]
]
'''


def four_sum(numbers, target):
  
  if type(numbers) is not list:
    raise TypeError('given numbers array must be a list.')

  if len(numbers) < 4:
    raise ValueError('given numbers array should have at least 4 elements.')
  
  for number in numbers:
    if type(number) is not int and type(number) is not float:
      raise ValueError('invalid values of given numbers')


  counts = dict()
  results = list()
  for number in numbers:
    try:
      counts[number] += 1
    except KeyError:
      counts[number] = 1
  uniques = sorted(counts.keys())
  
  for i in range(len(uniques)):
    for j in range(i+1, len(uniques)):
      for k in range(j+1, len(uniques)):
        
        # 4 0 0
        if uniques[i]*4 == target and counts[uniques[i]] >= 4: 
          results.append([uniques[i]]*4)
        # 3 1 0
        if uniques[i]*3 + uniques[j] == target and counts[uniques[i]] >=3:
          results.append( [uniques[i]]*3 + [uniques[j]] )
        # 3 0 1
        if uniques[i]*3 + uniques[k] == target and counts[uniques[i]] >=3:
          results.append( [uniques[i]]*3 + [uniques[k]])
        # 2 2 0
        if uniques[i]*2 + uniques[j]*2 == target and counts[uniques[i]] >=2 and counts[uniques[j]] >=2:
          results.append( [uniques[i]]*2 + [uniques[j]]*2)
        # 2 0 2
        if uniques[i]*2 + uniques[k]*2 == target and counts[uniques[i]] >=2 and counts[uniques[k]] >=2:
          results.append( [uniques[i]]*2 + [uniques[k]]*2)
        # 2 1 1
        if uniques[i]*2 + uniques[j] + uniques[k] == target and counts[uniques[i]] >=2:
          results.append( [uniques[i]]*2 + [uniques[j]] + [uniques[k]] )
        # 1 3 0
        if uniques[i] + uniques[j]*3 == target and counts[uniques[j]] >=3:
          results.append( [uniques[i]] + [uniques[j]]*3)
        # 1 0 3
        if uniques[i] + uniques[k]*3 == target and counts[uniques[k]] >=3:
          results.append( [uniques[i]] + [uniques[k]]*3)
        # 1 2 1
        if uniques[i] + uniques[j]*2 + uniques[k] == target and counts[uniques[j]] >=2:
          results.append( [uniques[i]] + [uniques[j]]*2 + [uniques[k]])
        # 1 1 2
        if uniques[i] + uniques[j] + uniques[k]*2 == target and counts[uniques[k]] >=2:
          results.append( [uniques[i]] + [uniques[j]] + [uniques[k]]*2 )  
        # 0 4 0
        if uniques[j]*4 == target and counts[uniques[j]]>=4:
          results.append( [uniques[j]]*4)
        # 0 3 1
        if uniques[j]*3 + uniques[k] == target and counts[uniques[j]]>=3:
          results.append( [uniques[j]]*3 + [uniques[k]])
        # 0 2 2
        if uniques[j]*2 + uniques[k]*2 == target and counts[uniques[j]]>=2 and counts[uniques[k]]>=2:
          results.append( [uniques[j]]*2 + uniques[k]*2)
        # 0 1 3
        if uniques[j] + uniques[k]*3 == target and counts[uniques[k]]>=3:
          results.append( [uniques[j]]+ [uniques[k]]*3)
        # 0 0 4
        if uniques[k]*4 == target and counts[uniques[k]]>=4:
          results.append( [uniques[k]]*4)
        
        l = target - uniques[i] - uniques[j] - uniques[k]
        try :
          if counts[l] > 0 and l > uniques[k]:
            results.append( [uniques[i]]+[uniques[j]]+ [uniques[k]]+[l])
        except KeyError:
          continue
  return results

if __name__ == '__main__':
  nums, target = [1, 0, -1, 0, -2, 2], 0
  r =  four_sum(nums, target)
  print(r)