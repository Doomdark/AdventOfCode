from collections import defaultdict, deque
from itertools import permutations

lines = open('13.in').read().splitlines()

guests = defaultdict(dict)

for line in lines:
    l = line.split()
    guest = l[0]
    other = l[10].replace('.','')
    amount = int(l[3])
    gainlose = -1 if l[2] == 'lose' else 1
    guests[guest][other] = amount * gainlose

def calc(guests):
    # Get all the possible seating orders
    maximum_happiness = 0
    for permute in permutations(guests.keys(), len(guests)):
        happiness = 0
        pd = deque(permute)
        for i in range(len(pd)):
            # To the right
            happiness += guests[pd[0]][pd[1]]
            # To the left
            happiness += guests[pd[0]][pd[-1]]
            # Rotate
            pd.rotate(1)
        maximum_happiness = max(maximum_happiness, happiness)
    return maximum_happiness

print('Part 1:', calc(guests))

## Part 2 ##

import copy
cguests = copy.copy(guests)
for k,v in guests.items():
    cguests[k]['Me'] = 0
    cguests['Me'][k] = 0

print('Part 2:', calc(cguests))
