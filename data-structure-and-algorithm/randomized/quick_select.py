import numpy as np
from random import choice
import matplotlib.pyplot as plt

arr = np.random.randint(1, 200, 501)
print(np.median(arr))
print(np.sort(arr)[250])

def quickselect(array, k, counter=0):
  pivot = choice(array)
  counter += len(array)
  left, right = [], []
  for e in array:  # the duplicate pivots were removed after the separation.
    if e < pivot: left += [e]
    if e > pivot: right += [e]
  # len(left) > k means k locates in the left sub array, go to the left sub array to find.
  if len(left) > k:
    return quickselect(left, k, counter)
  # otherwise k locates in the right sub array, 
  # need to reset the k by deducing the length of the left sub array.
  k = k - len(left)
  duplicates = len(array) - (len(left) + len(right)) # duplicates refer to the numbers of the duplicate pivot.
  if duplicates > k: # duplicates > k means nothing left in the right sub array, the pivot is the median.
    return pivot, counter
  else: 
    # deduce the length of pivot from the k, go to the right sub array to find the median.
    k = k - duplicates
    return quickselect(right, k, counter)

# median, counter= quickselect(arr, len(arr)//2)

# print(f'median = {median}, counter = {counter}')

# results = list()
# for run in range(1000):
#     n = 1001
#     series = [np.random.randint(1,500) for i in range(n)]
#     median,count = quickselect(series, n//2)
#     assert(median==np.median(series))
#     results.append(count)

# print(f'mean of operations = {np.mean(results)}')

# plt.hist(results, bins='auto')
# plt.xlabel("Computations")
# plt.ylabel("Frequency")
# plt.show()

input_size = [501, 1001, 5001, 10001, 20001, 50001]
computations = list()
for n in input_size:
    results = list()
    for run in range(1000):
        series = [np.random.randint(1, 25) for i in range(n)]
        median,count = quickselect(series, n//2)
        assert(median==np.median(series))
        results.append(count)
    computations.append(np.mean(results))
plt.plot(input_size, computations, '-o')
plt.xlabel("Input size")
plt.ylabel("Number of computations")
plt.show()