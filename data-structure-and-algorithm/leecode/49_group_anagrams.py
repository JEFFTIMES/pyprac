'''
Given an array of strings, group anagrams together. Example:
   
Input: ["eat", "tea", "tan", "ate", "nat", "bat"],
Output:
[
  ["ate","eat","tea"],
  ["nat","tan"],
  ["bat"]
]
'''

def create_dict(word):
  d =  dict()
  for letter in word:
    d[letter] = 1
  return d

def is_anagrams(word, dictionary):
  for letter in word:
    try :
      if dictionary[letter] == 1:
        pass
    except KeyError:
      return False
  return True

def group_anagrams(words):
  
  if type(words) is not list:
    raise TypeError('words is not a list.')
  if len(words) == 0:
    raise ValueError('empty list of words.')

  dictionaries = list()
  anagrams = dict()
  for word in words:
    existed = False
    # for each word, checks is_anagrams with each d in the dictionaries, if yes
    # add the word to the anagrams[d], set existed flag to True and break.
    for d in dictionaries:
      if is_anagrams(word, d):
        anagrams[str(d)] += [word]
        existed = True
        break
  
    # if existed flag is False, create a new d in dictionaries with the word add to anagrams[d]
    if not existed:
      d = create_dict(word)
      dictionaries.append(d)
      anagrams[str(d)] = [word]

  return anagrams.values()

# this version sorts each word and create a map with the sorted word as the key  
def group_anagrams_2(words):
  
  dictionary =  dict()
  for word in words:
    try:
      dictionary[''.join(sorted(word))] += [word]
    except KeyError:
      dictionary[''.join(sorted(word))] = [word]
  return dictionary.values()


if __name__ == '__main__':
  words = ["eat", "tea", "tan", "ate", "nat", "bat"]
  anagrams =group_anagrams_2(words)
  print(anagrams)