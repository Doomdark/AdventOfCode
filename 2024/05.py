lines = open("05.in").read().splitlines()

from collections import defaultdict

rules = defaultdict(list)
orders = []

for line in lines:
    if '|' in line:
        l,r = line.split('|')
        rules[l].append(r)
    elif ',' in line:
        order = line.split(',')
        orders.append(order)

# Process the orders
total = 0
incorrects = []
for order in orders:
    correct = True
    for c in range(len(order)-1):
        # Dictionary key
        item = order[c]
        # Following items
        remaining = order[c+1:]
        correct = True
        # Check each remaining item in  the list
        for thing in remaining:
            # Is this rule in the list of rules for item?
            if thing not in rules[item]:
                correct = False
                break
        if not correct:
            break
    if not correct:
        # Add any incorrect orders to the list for part 2
        incorrects.append(order)
        continue
    # Add up the middle item in the correct orders
    middle = len(order)//2
    total += int(order[middle])

print('Part 1:', total)

# Find the correct order for the incorrect orders

def sort(order):
    correct = False
    while(not correct):
        _order = order[:]
        correct = True
        for c in range(len(order)-1):
            # Dictionary key
            item = order[c]
            # Following items
            remaining = order[c+1:]
            # Check each remaining item in  the list
            for thing in remaining:
                # Is this rule in the list of rules for item?
                if thing not in rules[item]:
                    correct = False
                    # Put the thing that's after the item to before it
                    _order = order[:]
                    deletion = _order.index(thing)
                    del _order[deletion]
                    _order.insert(c, thing)
                    break
            #  The order isn't correct so run it again
            if not correct:
                order = _order
                break
    # The order is correct now
    middle = len(order)//2
    return int(order[middle])

total = sum([sort(order) for order in incorrects])

print('Part 2:', total)
