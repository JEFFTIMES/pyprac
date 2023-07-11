'''
Implement pow(x, n), which calculates x raised to the power n (xn).
'''
# x ^ n = (x ^ (n/2)) * 2, break down to the base case while n == 0 or n == 1
# the follow up process return x*x when the base n == 0, otherwise return x*x*x
# if n < 0, x = 1/x 

def pow_x_to_n(x, n):
  if n == 0:
    return 1
  if n < 0:
    x = 1/x
  r = recursively_pow(x, n)
  return r


def recursively_pow(x, n):

  # the base case: 
  if n == 1 or n == 0:
    return x

  y = recursively_pow(x, n//2)

  if n%2 == 0:
    return y*y
  else:
    return y*y*x

print(pow_x_to_n(2,8))