from functools import cmp_to_key
from collections import defaultdict
import itertools

lines = open('07.in').read().splitlines()

order = '23456789TJQKA'

types = ['high', 'pair', 'two pair', 'three', 'full house', 'four', 'five']

hands = {}

# Part 1 first
part2 = False

def get_type(hand):
    cards = defaultdict(int)
    # Count the different types of card
    for card in hand: cards[card] += 1

    # How many different cards?
    if   len(cards.keys()) == 5: return 'high'
    elif len(cards.keys()) == 4: return 'pair'
    elif len(cards.keys()) == 3: return 'three' if 3 in cards.values() else 'two pair'
    elif len(cards.keys()) == 2: return 'four'  if 4 in cards.values() else 'full house'
    else:                        return 'five'

def get_type2(hand):
    # Any Jokers in the hand?
    if 'J' in hand:
        # Track the highest hand we can make
        highest = 0
        # Replace all the J's with different cards to see which hand is the highest that can be made
        all_combs = itertools.combinations_with_replacement(order[1:], hand.count('J'))
        # Remove all the J's
        _hand = hand.replace('J','')
        # For each combination
        for comb in all_combs:
            # Glue the new card combo into the remaining card spaces
            h = _hand + ''.join(comb)
            # Get the type for the new hand
            hand_type = get_type(h)
            # Store the highest type
            highest = max(types.index(hand_type), highest)
        return types[highest]
    else:
        return get_type(hand)

def hand_sorter(l,r):
    hand_type_l = get_type(l) if not part2 else get_type2(l)
    hand_type_r = get_type(r) if not part2 else get_type2(r)
    # Compare hands
    if   types.index(hand_type_l) > types.index(hand_type_r): return -1
    elif types.index(hand_type_l) < types.index(hand_type_r): return  1
    else: # Hands are the same type
        # Grade by positional card value
        for _l,_r in zip(l,r):
            if   order.index(_l) > order.index(_r): return -1
            elif order.index(_l) < order.index(_r): return  1
    # They're the same
    return 0

# Make the hands from the input
for line in lines:
    _hand, bid = line.split()
    hands[_hand] = int(bid)

# Zero to start with
total = 0

# Sort the hands and accumulate the answer
for i,hand in enumerate(sorted(hands.keys(), key=cmp_to_key(hand_sorter), reverse=True)):
    total += (i+1) * hands[hand]

print('Part 1:', total)

# Part 2

# J is now the lowest value card - Joker, not Jack
order = 'J23456789TQKA'

# We're doing part 2
part2 = True

# Reset the total
total = 0

# Do the sort again
for i,hand in enumerate(sorted(hands.keys(), key=cmp_to_key(hand_sorter), reverse=True)):
    total += (i+1) * hands[hand]

print('Part 2:', total)
