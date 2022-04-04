

from numpy import r_


def roman_to_integer(roman_str):

  if type(roman_str) is not str:
    raise TypeError('input roman number should be a string')
  for c in roman_str:
    if c.upper() not in 'IVXLCDM':
      raise ValueError('roman number should be represented in combinations of I,V,X,L,C,D,M.')
  
  r_to_i = {
    'I' : 1,
    'IV': 4, 
    'V' : 5,
    'IX': 9,
    'X' : 10,
    'XL': 40,
    'L' : 50,
    'XC': 90,
    'C' : 100,
    'CD': 400,
    'D' : 500,
    'CM': 900,
    'M' : 1000
  }

  comb = ['IV', 'IX', 'XL', 'XC', 'CD', 'CM']
  roman = roman_str.upper()
  r_digit = ''
  integer = 0
  duplicates = []

  for c in roman:
    # start for a new roman digit
    if r_digit == '':
      r_digit = c
      continue
    # find the 2 letter digit
    if r_digit + c in comb:
      r_digit += c
      integer += r_to_i[r_digit]
      r_digit = ''
      continue
    # check syntax error
    duplicates.append(r_digit)
    integer += r_to_i[r_digit]
    r_digit = c
  if r_digit:
    integer += r_to_i[r_digit]

  return integer

if __name__ == '__main__':
  r = roman_to_integer('MMMCMXCIV')
  print(r)

