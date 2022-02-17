def lwz_text_compress(content, encoding):
  #generate encoding dictionary
  dictionary = { bytes([k]): k for k in range(256) } # take the bytes of the subsequence as the keys.
  print(dictionary)
  compressed = list()
  utf_8_encoded_bytes = content.encode(encoding)
  print(len(list(utf_8_encoded_bytes)))

  s = [utf_8_encoded_bytes[0]]
  for c in utf_8_encoded_bytes[1:]:   # checking each byte of the sequence
    if bytes( s + [c]) in dictionary: # if the subsequence s + [c] is in dictionary, extend s to s + [c]
      s = s + [c]
    else:   # s + [c] is a new sub sequence, put it in dictionary
      dictionary[bytes(s+[c])] = max(dictionary.values()) + 1   # encode the new subsequence 1 bigger than the largest one existed.
      print(f'new subsequence {bytes(s+[c])} encoded as: {dictionary[bytes(s+[c])]}')
      
      compressed.append(dictionary[bytes(s)])   #encode the new subsequence s
      s = [c]     # let s start from new position to find the new subsequence
  compressed.append(dictionary[bytes(s)]) 
  return compressed

def lwz_text_decompress(encoded, encoding):
  decompressed = list()
  reversed_dictionary = { k : bytes([k]) for k in range(256)}
  current = encoded[0]
  decompressed += reversed_dictionary[current]
  for element in encoded[1:]:
    # print(reversed_dictionary)
    previous = current
    current = element
    if current in reversed_dictionary.keys():
      s = reversed_dictionary[current]
      decompressed += s
      new_key = max(reversed_dictionary.keys()) + 1 # generating new key:value as well as processing the decoding.
      new_subsequence = reversed_dictionary[previous] + bytes([s[0]])
      reversed_dictionary[new_key] = new_subsequence
    else: # the encoded list contains a sumsequence which composed by repeating same element
      s = reversed_dictionary[previous] + bytes([reversed_dictionary[previous][0]])
      decompressed += s
      new_key = max(reversed_dictionary.keys()) +1
      new_subsequence = s
      reversed_dictionary[new_key] = new_subsequence
  return bytes(decompressed).decode(encoding)

txt = 'aaaababcababcdabc abcd 中文中文中文中文'

c = lwz_text_compress(txt, 'utf-8')
print(len(c),c)

d = lwz_text_decompress(c,'utf-8')
print(d)

print( len(c) / len(txt.encode('utf-8')) )