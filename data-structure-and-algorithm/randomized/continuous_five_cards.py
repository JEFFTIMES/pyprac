from random import choice, seed, randint, shuffle

# randomly draw 5 cards from a poker deck, check if the cards is a continuous set.
# joker could be treat as any card.

def check_skips(nonzero_sorted_cards):
  start = nonzero_sorted_cards[0]
  skips = 0
  for i in range(1, len(nonzero_sorted_cards)):
    if nonzero_sorted_cards[i] == start:
      return float('inf')
    if nonzero_sorted_cards[i] - start > 1:
      skips += nonzero_sorted_cards[i] - start
      start = nonzero_sorted_cards[i]
  return skips-1

def divide_cards(sorted_set):
  zero_cards = []
  nonzero_sorted_cards = []
  for card in sorted_set:
    if card == 0:
      zero_cards.append(card)
    else:
      nonzero_sorted_cards.append(card)
  return zero_cards, nonzero_sorted_cards

def is_continuous_set(cards):
  sorted_set = sorted(cards)
  zero_cards, nonzero_sorted_cards = divide_cards(sorted_set)
  skips = check_skips(nonzero_sorted_cards)
  if skips <= len(zero_cards):
    return True, sorted_set
  else:
    return False, sorted_set


if __name__ == '__main__':
  deck = [0]*2 + [i for i in range(1,14)]*4
  f = False
  t = 0
  while not f:
    copy_deck = [*deck]
    shuffle(copy_deck)
    for i in range(10):
      set = []
      for j in range(5):
        set.append(copy_deck.pop(0))
      f, sorted_set = is_continuous_set(set)
      t +=1
      print(t, f, sorted_set)
      