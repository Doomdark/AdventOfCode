from collections import defaultdict

lines = open('10.in').read().splitlines()

Grid  = defaultdict()

max_r = 0
max_c = 0

# Grid directions
dirs = {'n':(-1,0), 'e':(0,1), 's':(1,0), 'w':(0,-1)}

for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if char == 'S':
            start = (r,c)
        Grid[(r,c)] = char
        max_c = max(c,max_c)
    max_r = max(r,max_r)

# Now determine what type of square S is
n,e,s,w=0,0,0,0

def resolve_s(d, loc, check):
    vals = dirs[d]
    nr,nc = loc[0]+vals[0], loc[1]+vals[1]
    if 0<=nr<=max_r and 0<=nc<=max_c:
        if Grid[(nr,nc)] in check:
            return 1

# Does S have a square n,e,s,w of it which should connect to it?
e = resolve_s('e', start, '-J7')
w = resolve_s('w', start, '-LF')
s = resolve_s('s', start, '|JL')
n = resolve_s('n', start, '|F7')

# What type of square is S?
if   n and e: Grid[start] = 'L'
elif s and e: Grid[start] = 'F'
elif n and w: Grid[start] = 'J'
elif s and w: Grid[start] = '7'
elif n and s: Grid[start] = '|'
elif e and w: Grid[start] = '-'

# OK, the grid is done. Traverse the pipe to figure out how long it is and then divide by 2 for part 1.
loop = set()
loop.add(start)

loc = start
moving = None

done = False
while not done:
    # Go in one of the directions from S
    r,c = loc
    # Not started moving yet
    if loc == start:
        if   Grid[loc] in '-FL' : moving = 'e'
        elif Grid[loc] in '|7'  : moving = 's'
        elif Grid[loc] in 'J'   : moving = 'n'
    else: # Already moving
        if Grid[loc] == 'F':
            if   moving == 'n': moving = 'e'
            elif moving == 'w': moving = 's'
        elif Grid[loc] == '7':
            if   moving == 'n': moving = 'w'
            elif moving == 'e': moving = 's'
        elif Grid[loc] == 'J':
            if   moving == 's': moving = 'w'
            elif moving == 'e': moving = 'n'
        elif Grid[loc] == 'L':
            if   moving == 's': moving = 'e'
            elif moving == 'w': moving = 'n'

    # Get the movement for the next location
    dr,dc = dirs[moving]

    # New location along the pipe
    loc = (r+dr,c+dc)
    
    # Back at the start of the loop
    if loc == start:
        done = True

    # Add this location to the set
    loop.add(loc)

print('Part 1:', len(loop)//2)

# Part 2

inside_count = 0

# How to switch from inside to outside and back
insides = {0:1, 1:0}

# Keep track of the number of pipe traversals and junction crossings for each row.
for r in range(max_r):
    # Keep track of if we're inside on this row
    inside = 0
    # Stack of matches for pipe corners
    last = ''
    # Traverse the row
    for c in range(max_c):
        # Character in this grid location
        v = Grid[(r,c)]
        # Is the location on the main loop?
        if not (r,c) in loop:
            inside_count += inside
            continue
        
        # If a pipe traverse is L-*7 pr F-*J then that's equivalent to |.
        if v == '|' or last+v in ['FJ', 'L7']:
            # We've changed state
            inside = insides[inside]
        # Starting pipe corner
        elif v in 'FL':
            # Store the pipe corner
            last = v
                    
print('Part 2:', inside_count)

