def partition(lst, pivot_index=0):
    
  less_than = []
  more_than = []

  # base case:
  if len(lst) == 1:
    return less_than, lst.pop(0), more_than
  
  # other cases:
  pivot = lst.pop(pivot_index)  
  for item in lst:
    if item < pivot:
      less_than.append(item)
    else:
      more_than.append(item) 
  return less_than, pivot, more_than
    
def quicksort(lst, pivot_index=0):
  if len(lst) <= 1:
    return lst
  less_than, pivot, more_than = partition(lst, pivot_index)
  return quicksort(less_than, pivot_index) + [pivot] + quicksort(more_than, pivot_index)


if __name__ == '__main__':
  a = [3,5,1,7,6,4,8,8,2,3,9,0]
  print(quicksort(a))
