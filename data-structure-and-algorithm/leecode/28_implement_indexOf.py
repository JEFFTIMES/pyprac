'''
Implement strStr().
Return the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack.

 
Input: haystack = "hello", needle = "ll"
Output: 2

 
Input: haystack = "aaaaa", needle = "bba"
Output: -1

Clarification:
What should we return when needle is an empty string? This is a great question 
to ask during an interview.
For the purpose of this problem, we will return 0 when needle is an empty string. 
This is consistent to C's strstr() and Java's indexOf().
'''

def indexOf(haystack, needle):
  
  if len(needle) == 0:
    return 0
  
  j = 0
  index = -1
  for i in range(len(haystack)):          # go through haystack to find the letter matches to the first letter of needle.
    if haystack[i] == needle[j]:
      index = i
      for k in range(1,len(needle)):      # work together through the the length of len(needle) to check the equality. 
        if haystack[i+k] != needle[j+k]:
          index = -1
          break
      if index != -1:
        return index
  return index

if __name__ == '__main__':
  haystack, needle = "hello", "ll"
  print(indexOf(haystack, needle))
