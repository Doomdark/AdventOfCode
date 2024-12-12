lines = open('12test5.in').read().splitlines()

from collections import defaultdict

regions = defaultdict(list)

max_r = len(lines)
max_c = len(lines[0])

def adjacent(area, r, c):
    count = 0
    for dr,dc in [(0,1), (0,-1), (1,0), (-1,0)]:
        nr,nc = r+dr,c+dc
        if (nr,nc) in area:
            count += 1
    return count

def flood(name, r, c):
    global lines
    Q = [(r,c)]
    AREA = set()
    while Q:
        r,c = Q.pop()
        AREA.add((r,c))
        for dr,dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            nr,nc = r+dr,c+dc
            if nr>=0 and nr<max_r and nc>=0 and nc<max_c:
                if (lines[nr][nc] == name) and ((nr,nc) not in AREA):
                    Q.append((nr,nc))
    return AREA

SEEN = set()
for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if (r,c) not in SEEN:
            AREA = flood(char, r, c)
            SEEN |= AREA
            regions[char].append(list(AREA))

def get_perimeter(area):
    total = 0
    for r,c in area:
        open_sides = 4-adjacent(area, r, c)
        total += open_sides
    return total

def get_area(area):
    return len(area)

total = 0
for name, area_list in regions.items():
    for area in area_list:
        _area = get_area(area)
        _perimeter = get_perimeter(area)
        total += _area * _perimeter

print('Part 1:', total)

# Direction if we were going straight on
left     = {(0,1):(-1,0),(-1,0):(0,-1),(0,-1):(1,0),(1,0):(0,1)}
straight = {(0,1):(0,1),(-1,0):(-1,0),(0,-1):(0,-1),(1,0):(1,0)}
right    = {(0,1):(1,0),(1,0):(0,-1),(0,-1):(-1,0),(-1,0):(0,1)}
D        = {(0,1):'>',(1,0):'v',(-1,0):'^',(0,-1):'<'}

def check(area, direction, loc, lloc):
    r,c = loc
    dr,dc = direction
    nr,nc = r+dr,c+dc
    if (nr,nc) in area and (nr,nc) != lloc:
        return True
    return False

def move(loc, direction):
    r,c = loc
    dr,dc = direction
    return (r+dr,c+dc)

import time

def get_sides(area):
    # Start at a corner as edges start there. We're counting the corners really.
    min_c = min([c for r,c in area])
    min_r = min([r for r,c in area if c == min_c])
    loc = (min_r, min_c)
    start = (min_r, min_c)
    # Start bt going along the row from left to right
    direction = (0,1)
    print('start:', start)
    corners = 0
    VISITED = set(start)
    lloc = start
    # Now we need to trace the edge
    # We can only turn 90 degrees so tracing needs to turn left first, then straight, then right.
    while True:
        turn = False
        nloc = loc
        ndirection = direction
        VISITED.add(loc)
        #time.sleep(0.2)
        # Try to turn first before we move
        # Does the left-hand square exist in the area?
        if check(area, left[direction], loc, lloc):
            turn = True
            ndirection = left[direction]
        # Straight on
        elif check(area, direction, loc, loc):
            pass
        # Always turn right if we can't turn left or move forward
        else:
            turn = True
            ndirection = right[direction]
        if not turn:
            lloc = loc
            nloc = move(loc, ndirection)
        if turn:
            corners += 1
        print(loc, nloc, D[direction], turn, D[ndirection], corners)
        if nloc == start and ndirection == (0,1):
            return corners, VISITED
        loc = nloc
        direction = ndirection

for line in lines:
    print(line)
    
total = 0

areas = set()

class Area:
    def __init__(self, name, area, sides):
        self.name = name
        self.area = area
        self.sides = sides

for name, area_list in regions.items():
    for area in area_list:
        # Get the sides counts
        print(name, area)
        _area = get_area(area)
        _sides, visited = get_sides(area)
        areas.add(Area(name, area, sides))
        #print(_area, _sides)
        #total += _area * _sides

# At this point we have all the outer side counts.
# Now we have to determine if any of the areas have sub-areas contained within them.
# Assume those sub-areas won't have sub-sub-areas...
for area1 in areas:
    for area2 in areas:
        if area1 == area2: continue
        # Test if area2 has all of its squares enclosed by any of area1's squares
        

print('Part 2:', total)
