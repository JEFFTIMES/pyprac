def trampoline(f):
    def wrapped(*args, **kwargs):
        result = f(*args, **kwargs)
        print(f'result:{result}')
        while callable(result):
            print(f'result before call:{result}')
            result = result()
            print(f'result after call:{result}')

        return result
    return wrapped

def factorial(n, acc=1):
    print(f'entering with n:{n}')
    if n == 0:
        return acc
    else:
        fa = lambda: factorial(n-1, n*acc)
        print(f'fa:{fa}, n:{n}')
        return fa

fact = trampoline(factorial)

print(fact(3))  # This will compute 1000! without exceeding the recursion depth limit.
