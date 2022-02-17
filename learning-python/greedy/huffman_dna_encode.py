from heapq import heappush, heappop, heapify
from collections import defaultdict, Counter
from random import shuffle, seed

# initialize the DNA sequence
generator = ['A']*50 + ['C']*30 + ['T']*15 + ['G']*5
sequence = ''
seed(10)
for i in range(1000):
  shuffle(generator)
  sequence += generator[0]

# count the frequencies of each nucleotide
frequencies = Counter(list(sequence))
# print(frequencies)

# initialize the heap
heap = [ [freq, [[ch, '']]] for ch, freq in frequencies.items() ]
heapify(heap)


# huffman encoding
while len(heap) > 1:
  print('heap: ',heap)
  # pop up the least two elements of the heap
  low = heappop(heap)
  high = heappop(heap)
  print('low: ',low, 'high: ',high)

  # prefix '0' to the smaller one, and '1' to the larger one.
  for encoding_pair in low[1]:
    print(encoding_pair)
    encoding_pair[1] = '0' + encoding_pair[1]
  for encoding_pair in high[1]:
    encoding_pair[1] = '1' + encoding_pair[1]
  
  # combine the low and high into a new element and push it back in the heap
  print('new node:',[ low[0]+high[0], low[1] + high[1] ] )
  heappush(heap, [ low[0]+high[0], low[1] + high[1] ] )


