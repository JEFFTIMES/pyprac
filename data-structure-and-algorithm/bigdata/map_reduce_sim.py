from calendar import c

from sympy import re
from text_source import *

import os
if os.name == "nt":
    #Safer multithreading on Windows
    from multiprocessing.dummy import Pool
else:
    #Multiprocessing on Linux,Mac
    from multiprocessing import Pool
from multiprocessing import cpu_count
from functools import partial

def from_local_file(file):
  with open(file, 'r') as f:
    text = f.read()
  words = ''.join([letter for letter in text if letter not in punctuation]).split()
  return text, words


# define the count_keywords() as the workpiece for the map function.
# the count_keywords() record a tuple (keyword,1) each time a keyword is encountered.
def count_keywords(words, keywords):
  counts = list()
  for word in words:
    for keyword in keywords:
      if keyword == word.lower():
          counts += [(keyword,1)]
  return counts

# define a partition() to partition the dataset.
def partition(dataset, number_of_partitions):

  # let each partition take one element more than the result of floor division, 
  # it makes sure the total elements are divided into the given number of partitions 
  # by shrinking the size of the last partition.
  offset = len(dataset)//number_of_partitions + 1 
  print(len(dataset), offset, number_of_partitions)
  partitions = [ dataset[i:i+offset] for i in range(0, len(dataset), offset) ]
  return partitions

# define the distribute() to dispatch the whole dateset to each core of the cpu
def distribute(map_func, dataset, cores):
  pool = Pool(cores)
  partitions = partition(dataset, cores)
  print([len(partitions[i]) for i in range(len(partitions))])

  results = pool.map(map_func, partitions)
  return results

# define the shuffle() function to simulate shuffle and sort actions on the results come from the map.
# it receives a list of lists consist of the records which count for the appearance of the given keywords.
# it returns a dictionary maps the list of records tuple as the value to the keyword as the key.
def shuffle(results):
  sorted_map = dict()
  for result in results:
    for keyword, value in result:
      try:
        sorted_map[keyword] += [(keyword,value)]
      except KeyError:
        sorted_map[keyword] = [(keyword,value)]
  return sorted_map 

def reduce(sorted_map):
  reduced = dict()
  for keyword, tuples in sorted_map.items():
    reduced[keyword] = sum( [appearance for keyword, appearance in tuples] )
  return reduced
# map

def test():

  # get the text from local file.
  text, words = from_local_file('./gutenberg.txt')
  print(text[:627])

  # get number of cores for parallel processing
  cores = cpu_count()
  print(f'you have {cores} to parallely process the load.')

  # define the keywords for counting.
  keywords = ['war','peace','life','death']

  # partial() the count function to initialize the keywords argument.
  count_keywords_with_args = partial(count_keywords, keywords=keywords)

  # map the jobs to all the cores.
  results = distribute(count_keywords_with_args, words, cores)
  print([len(sub) for sub in results])
  
  # shuffle
  sorted_map = shuffle(results)
  print(sorted_map.keys())
  
  # reduce
  reduced = reduce(sorted_map)
  print(reduced)


if __name__ == '__main__':
  test()