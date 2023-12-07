lines = open('18.in').read().splitlines()

on = set()

for r,row in enumerate(lines):
    for c,char in enumerate(row):
        if char == '#':
            on.add((r,c))

R = r+1
C = c+1

import copy
on_copy = copy.copy(on)

def draw(on):
    print('-'*20)
    for r in range(R):
        row = ''
        for c in range(C):
            if (r,c) in on: row += '#'
            else: row += '.'
        print(row)

def get_neighbours(on, rc):
    non = []
    r,c = rc
    for dr,dc in [(-1,-1),(-1,0),(-1,1),
                  (0,-1),(0,1),
                  (1,-1),(1,0),(1,1)]:
        nr,nc = r+dr,c+dc
        if 0<=nr<R and 0<=nc<C:
            if (nr,nc) in on:
                non.append((nr,nc))
    return non

def update(on):
    new_on = set()
    # Iterate over the grid
    for r in range(R):
        for c in range(C):
            neighbours_on = get_neighbours(on, (r,c))
            # We're currently on
            if (r,c) in on:
                if len(neighbours_on) in [2,3]:
                    new_on.add((r,c))
            else:
                if len(neighbours_on) == 3:
                    new_on.add((r,c))

    return new_on

for i in range(100):
    on = update(on)

print('Part 1:', len(on))

on = on_copy

for i in range(100):
    on = update(on)
    # make sure the corners are all on for part2
    on.add((0,0))
    on.add((R-1,C-1))
    on.add((R-1,0))
    on.add((0,C-1))

print('Part 2:', len(on))
