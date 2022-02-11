import codecs
import hashlib
md5 = hashlib.md5()
md5.update('do something.'.encode('ascii'))
bytes_obj = md5.digest()

# type 'bytes' represents content with an escaped string, 
# under the hood the elements of types obj are integers range' 0-255.
print(type(bytes_obj), type(bytes_obj[0]), len(bytes_obj), bytes_obj, bytes_obj[0])

# convert a 'bytes' object to a list of integers, in which each integer represents 
# a byte with decimal integer value.
def bytes_to_ints(bytes_obj):
  return list(bytes_obj)


# covert a list of integers to a bytes object
def ints_to_bytes(ints):
  return bytes(ints)


# convert a bytes object to a list of strings, each string represents 
# the value of a byte in hexdecimal
def bytes_to_hex_list(bytes_obj):
  return [ hex(b) for b in bytes_obj ]


# convert a hex-string-represented-element list to a list with corresponding integer element.
def hex_list_to_ints(hex_str_repr_list):
  return [ int(h, 16) for h in hex_str_repr_list ]


# convert a bytes object to a hex-represented-string, in which every 2 chars represents 
# the integer value of the corresponding byte of the bytes object in hexdecimal without 0x prefix.
def bytes_to_hex_str(bytes_obj):
  return codecs.encode(bytes_obj, 'hex').decode('ascii') 


# the same as the above one
def bytes_to_hex_str2(bytes_obj):
  return ''.join([hs.lstrip('0x') if len(hs.lstrip('0x'))==2 else '0'+hs.lstrip('0x') for hs in [hex(b) for b in bytes_obj]])


# convert a hex-presented-string to a bytes object
def hex_str_to_bytes(hex_str):
  hsl = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
  return bytes([int(h, 16) for h in hsl ])


def test():
  ints = bytes_to_ints(bytes_obj)
  print(ints)

  hex_str = bytes_to_hex_str(bytes_obj)
  print(hex_str)

  hex_str2 = bytes_to_hex_str2(bytes_obj)
  print(hex_str2)

  hex_list = bytes_to_hex_list(bytes_obj)
  print(hex_list)

  to_bytes = ints_to_bytes(ints)
  print(to_bytes)

  to_bytes = ints_to_bytes(hex_list_to_ints(hex_list))
  print(to_bytes)

  to_bytes = hex_str_to_bytes(hex_str2)
  print(to_bytes)

if __name__ == '__main__':
  test()