
def longest_non_duplicate_sub_string(string):
  if string is None or len(string) == 0:
    raise ValueError('string should be not None or empty string.')
  
  index_of_char = dict()
  pre_char = string[0]
  index_of_char[pre_char] = 0
  pre_length = 1
  max_sub_length = 0
  max_sub_str = ''

  for i in range(1, len(string)):
    cur_char= string[i]
    try:        
      distance = i - index_of_char[cur_char]    # if cur_char exists in the dict, that means current char repeats one of the previous chars, 
      if distance > pre_length:                 # get the distance between the repeated two. if the distance > pre_length, the previous one 
        pre_length += 1                         # of this char is out the range of the repeation of the i-1 char, so this char could be added
      else:                                     # to the none repeat sub string.
        pre_length = distance                   # otherwise, reset the pre_length to the distance of this char to its previous one.
      index_of_char[cur_char] = i                
    except KeyError:                            # if cur_char does not exists in the dict, that means it is a new char, add it to the dict
      index_of_char[cur_char] = i               # and add 1 to pre_length.
      pre_length += 1

    if max_sub_length < pre_length:             # save the longest sub string and its length.
      max_sub_length = pre_length
      max_sub_str = string[i-pre_length+1:i+1]
  
  return max_sub_length, max_sub_str

a = 'abcdefabcdefgh'

l, str = longest_non_duplicate_sub_string(a)
print(l,str)