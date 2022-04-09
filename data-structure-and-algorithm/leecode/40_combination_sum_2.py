'''
Given a collection of candidate numbers ( candidates ) and a target number ( target ), find all unique combinations in candidates where the candidate numbers sums to target .
Each number in candidates may only be used once in the combination. Note:
All numbers (including target ) will be positive integers. The solution set must not contain duplicate combinations.

Example 1:
Input: candidates = [10,1,2,7,6,1,5], target = 8,
A solution set is:
[
  [1, 7],
  [1, 2, 5],
  [2, 6],
  [1, 1, 6]
]

'''

def combination_sum_2(candidates, target):

  solutions = list()
  start = 0
  recursive_combination_sum_without_repeat_number(sorted(candidates), target, start, solutions)
  print(solutions)

def recursive_combination_sum_without_repeat_number(candidates, target, start, solutions, solution=[]):

  # the base case:
  if target == 0:
    solutions += [solution[:]]
    return
  if target < 0:
    return


  for i in range(start, len(candidates)):
    
    # if ith number is not the starting and it equals to the previous number, skips it.
    if i > start and candidates[i] == candidates[i-1]:
      continue
    
    number = candidates[i]

    if number > target:
      break
    solution.append(number)

    recursive_combination_sum_without_repeat_number(candidates, target-number, i+1, solutions, solution)

    solution.pop()

if __name__ == '__main__':
  
  candidates, target = [10,1,2,2,7,6,1,5], 8
  solutions = []
  
  combination_sum_2(candidates, target)
  print(solutions)