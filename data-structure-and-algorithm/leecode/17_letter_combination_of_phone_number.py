'''
Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent.
phone number keypad: { 2: 'abc', 3:'def', 4:'ghi', 5:'jkl', 6:'mno', 7:'pqrs', 8:'tuv', 9:'wxyz'}
'''

def gen_numbers_to_letters(numbers):
  
  n_to_l = { '2': 'abc', '3':'def', '4':'ghi', '5':'jkl', '6':'mno', '7':'pqrs', '8':'tuv', '9':'wxyz'}
  
  if len(numbers) == 1:
    for l in n_to_l[numbers]:
      yield l
    return

  for l in n_to_l[numbers[0]]:
    for s in gen_numbers_to_letters(numbers[1:]):
      yield l + s

def numbers_to_letters(numbers):
  try:
    for n in str(numbers):
      if n not in '23456789':
        raise ValueError('number should be in 2-9.')
  except TypeError:
    print('input must be a number or a string of numbers.')
    return
  return gen_numbers_to_letters(str(numbers))


if __name__ == '__main__':
  ge = numbers_to_letters(2345)
  print([c for c in ge])