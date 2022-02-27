from random import choice, seed, randint, shuffle
import matplotlib.pyplot as plt


balls = { i: 1 for i in range(1,11) }

# create the set of balls each time
urn = []
for ball, duplicates in balls.items():
  urn += [ball for i in range(duplicates)]
print(urn)

# draw a ball from urn randomly
shuffle(urn)

ball = choice(urn)
balls[ball] += randint(1,3)

