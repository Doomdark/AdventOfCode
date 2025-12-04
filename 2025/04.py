# Read the input
lines = open("04.in").read().splitlines()

dirs = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

R = len(lines)
C = len(lines[0])

# Make a set of rolls
rolls = set()

for r in range(R):
    for c in range(C):
        if lines[r][c] == '@':
            rolls.add((r,c))

movable = 0

# How many are movable?
for r, c in rolls:
    adjs = 0
    for dr, dc in dirs:
        nr, nc = dr+r, dc+c
        # Off-grid check
        if 0 <= nr < R and 0 <= nc < C:
            if (nr,nc) in rolls:
                adjs += 1
    # Fewer than 4 adjacents means it can be moved
    if adjs < 4:
        movable += 1

print('Part 1:', movable)

def get_removable(ROLLS):
    removable = set()
    for r,c in ROLLS:
        adjs = 0
        for dr, dc in dirs:
            nr, nc = dr+r, dc+c
            # Off-grid check
            if 0 <= nr < R and 0 <= nc < C:
                if (nr,nc) in ROLLS:
                    adjs += 1
        # Fewer than 4 adjacents means it can be removed
        if adjs < 4:
            removable.add((r,c))
    return removable

remove = True
total_removed = 0

# Iterate until there are no more removable rolls
while remove:
    remove = get_removable(rolls)
    total_removed += len(remove)
    # Subtract the removable set from the set of rolls
    rolls -= remove

print('Part 2:', total_removed)
