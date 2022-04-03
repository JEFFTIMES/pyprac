import numpy as np
from random import choice
import matplotlib.pyplot as plt



def quickselect(array, k, counter=[0]):
  pivot = choice(array)
  counter[0] += len(array)
  left, right = [], []
  
  # the duplicated pivots were not moved in left[] or right, need to be removed after the division.
  for e in array:  
    if e < pivot: left += [e]
    if e > pivot: right += [e]
  
  # len(left[]) > k means the kth number locates in the left sub array, go to the left sub array to find.
  if len(left) > k:
    return quickselect(left, k, counter)
  
  # otherwise k locates in the right sub array, or in the duplicates.
  # there are k - len(left[]) numbers less than k locate in the right sub array, or in the duplicates
  # reset the k by reduce the length of the left sub array from k.
  k = k - len(left)

  # the function moves the less than to the left[] and the more than to the right[],
  # there are the numbers equal to the pivot number should be deducted before the starting 
  # of the next iteration.
  duplicates = len(array) - (len(left) + len(right)) 
  
  # if the number of duplicates pivots is more than the adjusted k, that means the k locates in the 
  # duplicate pivots [], the pivot itself is the kth number.
  # otherwise, reduces the number of duplicate pivots from k, goes in to the right sub array to find 
  # the kth number.
  if duplicates > k: 
    return pivot, counter
  else: 
    # reduce the number of duplicate pivots from the k, go to the right sub array to find the median.
    k = k - duplicates
    return quickselect(right, k, counter)



# arr = [np.random.randint(1, 25) for i in range(5001)]
# print(np.median(arr))
# print(np.sort(arr)[len(arr)//25])
# median, count = quickselect(arr, len(arr)//2)
# print(median, count)

input_size = [501, 1001, 5001, 10001, 20001, 50001]
computations = list()
for n in input_size:
    results = list()
    for run in range(1000):
        series = [np.random.randint(1, 25) for i in range(n)]
        median,count = quickselect(series, n//2)
        assert(median==np.median(series))
        results.append(count[0])
    computations.append(np.mean(results))
plt.plot(input_size, computations, '-o')
plt.xlabel("Input size")
plt.ylabel("Number of computations")
plt.show()