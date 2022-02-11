from sklearn.model_selection import learning_curve
from custom_hash import custom_hash_f
from random import randint
from bytes_converters import *

hash_functions = 3
bit_vector_length = 131
bit_vector = [0] * bit_vector_length

def insert_to(payload):
  bit_pos = list()
  for i in range(hash_functions):
    pos = custom_hash_f(payload, i, bit_vector_length)
    bit_vector[pos] = 1
    bit_pos += [pos]
  print(f'insert the hash of payload to positions {bit_pos}')

def check(payload):
  bit_pos_checked = []
  for i in range(hash_functions):
    pos = custom_hash_f(payload, i, bit_vector_length)
    bit_pos_checked += [bit_vector[pos]]
  print(f'all {hash_functions} positions checked: {bit_pos_checked}')
  s = sum(bit_pos_checked)
  if s < hash_functions:
    return 'Not in'
  else: 
    return 'Possible in'

# 20 strings with random length from 20 to 100 random ascii chars.
inputs = [ints_to_bytes([randint(0,127) for i in range(randint(20,100))]).decode('ascii') for j in range(20)]
to_check = [ints_to_bytes([randint(0,127) for i in range(randint(20,100))]).decode('ascii') for j in range(200)]

for s in inputs:
  insert_to(s)
  print(f'bit_vector: {bit_vector}')

# for s in inputs:
#   print(check(s))

for ck in to_check:
  print('new:',check(ck))