
# anytime when the Memoize(func) is called, it instansiates a callable object
# as a wrapper function for the passed in function.
class Memoize():
  def __init__(self, f):
    self.cache = dict()
    self.func = f
  def __call__(self, *args):
    if args not in self.cache.keys():
      self.cache[args] = self.func(*args)
    return self.cache[args]


def fibonacci(n):
  if n<2:
    return 1
  else:
    print('loading...')
    return fibonacci(n-1) + fibonacci(n-2)

fib = Memoize(fibonacci)


print(fib(5))
print(fib(5))
print(fib(6))