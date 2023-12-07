from collections import defaultdict

lines = open('03.in').read().splitlines()

numbers = {}
symbols = {}

max_c, max_r = 0,0

# Read the numbers and symbols in an store their locations
for r,line in enumerate(lines):
    number = ''
    for c,char in enumerate(line):
        if char.isdigit():
            number += char
        else: # Not a number - save the number
            if number != '':
                for i in range(len(number)):
                    numbers[(r,c-i-1)] = int(number)
            number = ''
            # The char is a symbol
            if char != '.':
                symbols[(r,c)] = char
        max_c = c

    # End of line. Check if there's a number in the string.
    if number != '':
        for i in range(len(number)):
            numbers[(r,max_c-i)] = int(number)

    max_r = r

# Get the adjacent squares
def get_adjacents(loc):
    r,c = loc
    adjs = []
    for dr,dc in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
        nr,nc = r+dr,c+dc
        if 0<=nr<=max_r and 0<=nc<=max_c:
            adjs.append((nr,nc))
    return adjs

total = 0

# Iterate throug hthe symbols and find their adjacent part numbers
for symbol in symbols.keys():
    parts = []
    adjs = get_adjacents(symbol)
    rows = defaultdict(list)
    for adj in adjs:
        if adj in numbers.keys():
            part = numbers[adj]
            row = adj[0]
            # Check that a duplicate number match is on a different row
            if part not in rows[row]:
                parts.append(part)
                rows[row].append(part)

    total += sum(parts)

print('Part 1:', total)

# Part 2

total = 0

# Iterate throug hthe symbols and find their adjacent part numbers
for symbol_loc, symbol in symbols.items():
    # Only consider gear symbols
    if symbol == '*':
        parts = []
        adjs = get_adjacents(symbol_loc)
        rows = defaultdict(list)
        for adj in adjs:
            if adj in numbers.keys():
                part = numbers[adj]
                row = adj[0]
                # Check that a duplicate number match is on a different row
                if part not in rows[row]:
                    parts.append(part)
                    rows[row].append(part)
        # Only consider gears with exactly 2 adjacent numbers
        if len(parts) == 2:
            total += parts[0] * parts[1]

print('Part 2:', total)
