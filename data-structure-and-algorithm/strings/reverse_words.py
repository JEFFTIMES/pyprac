# given a sentence, reverse the words of the sentence but not the letters of words.

def reverse_words(s):
  if not type(s) is str:
    raise TypeError('s must be a string.')
  if len(s) == 0:
    raise ValueError('given string should not be empty string.')
  words =  s[::-1].split(' ')
  for index, word in enumerate(words):
    word = word[::-1]
    words[index] =word
  return ' '.join(words)


def reversed_by_letter(ls, start, end):
  while start < end: 
    t = ls[start]
    ls[start] = ls[end]
    ls[end] = t
    start += 1
    end -= 1

def reverse_words_with_pointer(s):
  ls = list(s)
  start, end = 0, len(ls)-1
  reversed_by_letter(ls, start, end)
  
  w_start, w_end = 0, 0
  while w_end <= len(ls):
    if ls[w_start] == ' ':   # align end with start when step on a new word.
      w_start += 1
      w_end = w_start
    elif w_end == len(ls):  # when w_end go out the string, reverse the last word.
      reversed_by_letter(ls, w_start, w_end-1)
    elif ls[w_end] == ' ':  # when w_end reach a space, reverse the word [w_start, w_end-1], and move w_start forward
      reversed_by_letter(ls, w_start, w_end-1)
      w_start = w_end
    w_end += 1

  return ''.join(ls)


if __name__ == '__main__':
  s = 'the words'

  r = reverse_words(s)
  print(r)
  print(s)
  r2 = reverse_words_with_pointer(s)
  print(r2)