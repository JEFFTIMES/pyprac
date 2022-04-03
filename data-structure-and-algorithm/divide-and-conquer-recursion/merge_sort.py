
def merge(array, start, next_start, end, dsc_pair_count=0):
  _L, _R = array[start: next_start], array[next_start: end+1]
  _L.append(float('inf'))
  _R.append(float('inf'))
  for i in range(start, end+1):
    if _L[0] <= _R[0]:
      array[i] = _L[0]
      _L.pop(0)
    else:
      dsc_pair_count += len(_L) # count the dsc_pair
      array[i] = _R[0]
      _R.pop(0)
  return dsc_pair_count


def merge_sort(array, start=None, end=None, count=0):
  if start is None and end is None:
    start, end = 0, len(array)-1
  
  # base case: 
  if end == start :
    return count

  # other cases: 
  next_start = (start + end + 1) >> 1     # next_start equal to the length of the left part subarray.
  merge_sort(array, start, next_start-1)  # here the index of the end element of the left part subarray equal to next_start-1
  merge_sort(array, next_start, end)
  count += merge(array, start, next_start, end, count)

  return count

a = [7,5,6,4]
count = merge_sort(a)
print(a, count)