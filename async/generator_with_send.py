def interactive_generator():
    value = yield "Start"  # Initial yield to kick off the generator
    print(f'in the g: {value}')
    while True:
        value = yield f"Received: {value}"
        print(f'in the while: {value}')

g = interactive_generator()
print(next(g))
print('---')
print(g.send(10))
print('---')
print(g.send(20))
print('---')
print(g.send(30))
print('---')