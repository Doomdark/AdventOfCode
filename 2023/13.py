import copy

lines = open('13.in').read().splitlines()

# Store the patterns
patterns = []
# Store the pattern dimensions
sizes = []
# Store the part 1 reflection scores for each pattern
scores = []
# Make a set of rocks
rocks = set()
# Row count
r = 0
# Max row/column count
max_r = 0
max_c = 0

# Process the lines
for line in lines:
    # Blank line -
    if line == '':
        # If we've got some rocks then add them to the patterns list
        if rocks:
            patterns.append(rocks)
            sizes.append((max_r+1, max_c+1))
            rocks = set()
            r = 0
            max_r = 0
            max_c = 0
    else:
        # Process this line of rocks
        for c,char in enumerate(line):
            if char == '#':
                rocks.add((r,c))
            # Keep track of max sizes
            max_c = max(max_c,c)
        # Keep track of max sizes
        max_r = max(max_r,r)
        # Next row
        r += 1

# If we've got rocks left then add them too
if rocks:
    patterns.append(rocks)
    sizes.append((max_r+1, max_c+1))

def match_rows(row, pattern, size):
    'Try to match rows starting from the provided row number'
    size_r = list(range(size[0]))
    # Get the list of up/down rows to compare. Reverse the up rows.
    u = list(reversed(size_r[:row+1]))
    d = size_r[row+1:]
    # Limit the row comparison to the smallest dimension
    minsize = min(len(u),len(d))
    up = u[:minsize]
    dn = d[:minsize]
    # Now compare each row pair in turn
    for u, d in zip(up,dn):
        ucols = set([c for x,c in pattern if x == u])
        dcols = set([c for x,c in pattern if x == d])
        if ucols != dcols:
            return False
    return True

def match_cols(col, pattern, size):
    'Try to match columns starting from he provided column number'
    size_c = list(range(size[1]))
    # Get the list of up/down columns to compare. Reverse the up rows.
    u = list(reversed(size_c[:col+1]))
    d = size_c[col+1:]
    # Limit the row comparison to the smallest dimension
    minsize = min(len(u),len(d))
    up = u[:minsize]
    dn = d[:minsize]
    # Now compare each row pair in turn
    for u, d in zip(up,dn):
        urows = set([r for r,x in pattern if x == u])
        drows = set([r for r,x in pattern if x == d])
        if urows != drows:
            return False
    return True

def find_reflection(pattern, size, score):
    'Find reflections in row and columns'
    size_r, size_c = size

    for r in range(size_r-1):
        if match_rows(r, pattern, size):
            val = (r+1) * 100
            if score != val:
                return val

    for c in range(size_c-1):
        if match_cols(c, pattern, size):
            val = c+1
            if score != val:
                return val

    # No reflections
    return 0

def part1():
    total = 0
    for i in range(len(patterns)):
        score = find_reflection(patterns[i], sizes[i], 0)
        # Keep track of the existing scores
        scores.append(score)
        total += score

    print('Part 1:', total)

part1()

# Part 2

# For each pattern, togglie each grid location and re-running the pattern matching

def print_pattern(r, c,pattern, size):
    size_r, size_c = size
    print('-'*10, r, c, '-'*10)
    for r in range(size_r):
        row = ''
        for c in range(size_c):
            if (r,c) in pattern:
                row += '#'
            else:
                row += '.'
        print(row)

def part2():
    total = 0
    # Iterate through all the patterns
    for i,p in enumerate(patterns):
        size_r, size_c = sizes[i]
        pattern_done = False
        # For each row/column toggle the grid location and re-run the matching.
        # If there's a match which isn't the original match then that's the new reflection.
        for r in range(size_r):
            for c in range(size_c):
                # For each new (r,c) copy the original pattern
                pattern = copy.deepcopy(p)
                # Modify the specific square
                if (r,c) in pattern:
                    pattern.remove((r,c))
                else:
                    pattern.add((r,c))
                # Now find the reflection that isn't the original one.
                score = find_reflection(pattern, sizes[i], scores[i])
                # If score is non-zero then we've found a reflection.
                if score > 0:
                    pattern_done = True
                    total += score
                if pattern_done: break
            if pattern_done: break

    print('Part 2:', total)

part2()
