# given a string, cut n numbers of letters from the left and append them to the end of the string.

# divide the string to two substrings, let the left one contains the n numbers of letters 
# reverse the two substrings respectively then reverse the whole string again it works as we need.


from reverse_words import reversed_by_letter 

def left_spin_n_letters(s, n):
  if not type(s) is str or not type(n) is int:
    raise TypeError('invalid string or number.')
  if n < 0 or n > len(s):
    raise ValueError('invalid value of given number.')

  ls = list(s)
  start, end = 0, n-1
  reversed_by_letter(ls, start, end)
  start, end = n, len(ls)-1
  reversed_by_letter(ls, start, end)
  reversed_by_letter(ls,0, len(ls)-1)
  return ''.join(ls)

if __name__ == '__main__':

  s = 'abcdefg'
  r = left_spin_n_letters(s, 3)
  print(r)