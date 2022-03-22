# there is a list of integer number, only 1 number appears once, each of the other numbers repeat itself 3 times
# find out the number appears once.
# suppose all the numbers in the list are 32bits integer

def number_appear_once(numbers):
  # sum up the corresponding bit of each number from 0th to 31st bit.
  bit_sums = [0 for i in range(32)]
  for number in numbers:
    mask = 1
    for i in range(31, -1, -1):
      bit = number & mask 
      if bit != 0:
        bit_sums[i] +=1
      mask = mask <<1
  print(bit_sums)

  for bit, value in enumerate(bit_sums):
    bit_sums[bit] = value %3
  print(bit_sums)

  n=0
  mask = 1
  for i in range(31, -1, -1):
    n += bit_sums[i]*mask
    mask = mask<<1
  print(n)

a = [11,11,11,22,22,22,5,44,44,44]
number_appear_once(a)