'''
Given a set of candidate numbers ( candidates ) (without duplicates) and a target number
( target ), find all unique combinations in candidates where the candidate numbers sums to
target .
The same repeated number may be chosen from candidates unlimited number of times.
Note:
All numbers (including target ) will be positive integers.
The solution set must not contain duplicate combinations.


Input: candidates = [2,3,6,7], target = 7,
A solution set is:
[
[7],
[2,2,3] ]


Input: candidates = [2,3,5], target = 8,
A solution set is:
[
  [2,2,2,2],
  [2,3,3],
  [3,5]
]

'''

def combination_sum(candidates, target):
  
  if type(candidates) is not list or (type(target) is not int and type(target) is not float):
    raise TypeError("candidates must be a list, target must be a number.")
  if len(candidates) == 0:
    raise ValueError("candidates must not be empty.")
  solutions = []
  start = 0
  recursively_combine_rmv_duplicates(sorted(candidates), target, start, solutions=solutions)
  return solutions


# this version of combination sum does not avoid the duplicates because it
# always start from the first number of the candidates to begin the search for
# each reduced target.  
def recursively_combine(candidates, target, solutions, solution=None, visited=[]):
  
  if solution is None:
    solution = []

  # the base case:
  if target == 0: 
    return True

  if target < 0:
    return False


  # the other cases:
  # (1) runs a for loop to choose a number from the candidates and saves it in the 
  # solution, then recursively calls the procedure with a reduced target = target-number.
  # (2) when the recursive call returns a True, means a solution found for the reduced 
  # target, save the solution. because all the number after current number are different
  # from each other, no solutions exist within the following numbers, break to skip the 
  # looping for them. 
  # (3) before leaves current number and goes for trying the next number for the reduced
  # target, restore the value of the target to its value that before reduced. restore
  # the solution to that current number isn't added.

  # (4) when the following returns a False, means no solution is found. does the clean job
  # and moves to the next number to process.
  for number in candidates:
    
    # (1)
    solution.append(number)
    target -= number 
    
    if recursively_combine(candidates, target, solutions, solution, visited):
      # (2) saves the solution
      solutions += [solution[:]]
      # (3)
      target += number
      solution.pop()
      # (2)
      break
      
    else:
      # (4)
      target += number
      solution.pop()


# this version of combination sum set a start pointer to indicate the procedure which number to begin
# the search for each reduced target, that avoids the duplicates for each reduced target.
def recursively_combine_rmv_duplicates(candidates, target, start, solutions, solution=None):

  if solution == None:
    solution = []

  # the base case:
  if target == 0:
    solutions += [solution[:]]
    return 
  if target < 0:
    return

  # the other cases:
  for i in range(start, len(candidates)):
    number = candidates[i]      # save the current number to solution
    if number > target:         # skip if the number is larger than the target
      break
    solution.append(number)
    # recursively call with reduced target and the non-visited number as the new start point
    recursively_combine_rmv_duplicates(candidates, target-number, i, solutions, solution) 
    solution.pop()

if __name__ == '__main__':
  candidates, target = [1,2,3,5,6,7], 5

  print(combination_sum(candidates, target))
