lines = open('11.in').read().splitlines()

galaxies = set()
empty_rows = set()
empty_columns = set()

max_r, max_c = 0,0

for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if char == '#':
            galaxies.add((r,c))
        max_c = max(c,max_c)
    max_r = max(r,max_r)

# Find which rows and columns are empty
all_c = [c for r,c in galaxies]
for c in range(max_c+1):
    if c not in all_c:
        empty_columns.add(c)

all_r = [r for r,c in galaxies]
for r in range(max_r+1):
    if r not in all_r:
        empty_rows.add(r)

def expand(g, amount=2):
    'The row/column is already 1 wide so subtract 1 from the provided number.'
    global empty_rows, empty_columns
    r,c = g
    # Extra rows/columns to add on
    er,ec = 0,0
    for row in empty_rows:
        if row < r:
            er += amount-1
    for col in empty_columns:
        if col < c:
            ec += amount-1
    return (r+er,c+ec)
    
def manhattan_distance(a,b):
    return abs(b[0]-a[0]) + abs(b[1]-a[1])

# Now find the shortest paths between all pairs of galaxies

def solve(part2=False):
    distances = {}
    width = 1000000 if part2 else 2
    for a in galaxies:
        for b in galaxies:
            # Don't test a galaxy against itself
            if a == b: continue
            # Make a unique galaxy pair ID string
            id = ''.join(sorted([str(a), str(b)]))
            # If we've already done this galaxy pair then skip it
            if id in distances: continue
            # Find the expanded coordinates for the two galaxies
            ea = expand(a, width)
            eb = expand(b, width)
            # Get the distance
            dist = manhattan_distance(ea, eb)
            # Store it
            distances[id] = dist
    return sum(distances.values())
            
print('Part 1:', solve())
print('Part 2:', solve(True))
