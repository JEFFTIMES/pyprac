# generating integers
def gen_ints(start):
    i=start
    while True:
        yield i
        i +=1
        
# eliminating multiples of given number n from given integer series
def eli_multiples(n,ints):
    for element in ints:
        if element % n != 0:
            yield element
            
# generating primes
def gen_primes():
    ints = gen_ints(2)
    while True:
        prime = ints.__next__()
        ints = eli_multiples(prime, ints)
        yield prime

def test():
  a = gen_primes()
  primes = [next(a) for i in range(100)]
  print(primes)

if __name__ == '__main__':
  test()


