'''
Given two integers dividend and divisor , divide two integers without using multiplication, division and mod operator.
Return the quotient after dividing dividend by divisor . The integer division should truncate toward zero.
'''


# the inner loop set the divisor with the double size of itself and compare the result with the dividend
# until the result just is not more than the dividend, record the times of the double size operations.
# let the dividend equals to substract the result from itself, then goes the inner loop again until
# the dividend less than the divisor. 
from sympy import div, true


def divide_two_integers(dividend, divisor):
  if dividend < divisor:
    return 0
  quotient = 0
  while dividend > divisor:
    sub_quotient = 1
    temp_divisor = divisor 
    while (temp_divisor<<1) <= dividend:
      temp_divisor <<= 1
      sub_quotient <<= 1
    quotient += sub_quotient
    dividend -= temp_divisor
  return quotient


if __name__ == '__main__':
  print(divide_two_integers(16,6))




