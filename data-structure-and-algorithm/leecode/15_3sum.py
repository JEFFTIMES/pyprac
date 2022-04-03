'''
  Given an array nums of n integers, are there elements a, b, c in nums such that a + b + c = 0? 
  Find all unique triplets in the array which gives the sum of zero.
  Note:
  The solution set must not contain duplicate triplets.
'''
import pprint

def three_sum(arr):
  three_sum = dict()
  for i in range(len(arr)-2):
    for j in range(i+1, len(arr)-1):
      for k in range(j+1, len(arr)):
        key = arr[i] + arr[j] + arr[k]
        value = set((i,j,k))
        if key == 0:
          try:
            duplicated = False
            for existed in three_sum[key]:
              if set((arr[i], arr[j], arr[k])).difference(set([ arr[i] for i in existed])) == set():
                duplicated = True
            if not duplicated:
              three_sum[key] += [value]
          except KeyError:
            three_sum[key] = [value]
  return [ [arr[i] for i in idx] for idx in three_sum[0] ]

def three_sum_2(arr):
  
  results = []
  # get the sorted unique number list, and the counts dict for counting the duplicate numbers.
  counts = dict()
  for n in arr:
    try:
      counts[n] += 1
    except KeyError:
      counts[n] = 1
  
  # sort the uniques to keep the finding of the k without duplicates.
  uniques = sorted(counts.keys())
  
  # try 3 sum with the numbers in the sorted list.
  for i in range(len(uniques)):
    for j in range(i+1, len(uniques)):
      
      # an unique ith with more than or equal to 3 duplicates
      if counts[uniques[i]] >= 3 and uniques[i] == 0:
        results.append( [uniques[i]]*3 )
      # an unique ith with more than 1 duplicates and an unique jth
      if counts[uniques[i]] >1 and uniques[i]*2 + uniques[j] == 0:
        results.append( [uniques[i]]*2 + [uniques[j]] )
      # an unique ith and an unique jth with more than 1 duplicates
      if counts[uniques[j]] >1 and uniques[i] + uniques[j]*2 == 0:
        results.append( [uniques[i]] + [uniques[j]]*2)
      # ith + jth does not equal to 0, but there exists a kth excepting ith and jth adds up the result to 0
      k = 0 - uniques[i] - uniques[j]
      try :
        # here the checking of k > uniques[j] is necessary to avoid outputing duplicated results
        if k > uniques[j] and counts[k] > 0 :
          results.append([uniques[i], uniques[j], k])
      except KeyError:
        continue

  return results

if __name__ == '__main__':
  nums = [-1, 0, 1, 2, -1, -4]     # solution [ [-1, 0, 1], [-1, 2, -1]]

  print(three_sum(nums))

  print(three_sum_2(nums))