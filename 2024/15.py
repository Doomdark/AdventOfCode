lines = open('15.in').read().splitlines()

from collections import defaultdict

walls = set()
boxes = defaultdict()
moves = ''
loc = None

# R and C used for the grid printing
R = 0
C = 0

for r,line in enumerate(lines):
    if not line: continue
    if line.startswith('#'):
        R = r
        for c,char in enumerate(line):
            C = c
            if   char == '#': walls.add((r,c))
            elif char == 'O': boxes[(r,c)] = 'O'
            elif char == '@': loc = (r,c)
    else:
        moves += line

R += 1
C += 1

MOVES = {'^':(-1,0), '>':(0,1), 'v':(1,0), '<':(0,-1)}

# Use a DFS to determine which boxes can move
def get_moveable(m,loc):
    dr,dc = m
    lr,lc = loc
    nr,nc = dr+lr,dc+lc
    moveable = []
    # Hit a wall?
    if (nr,nc) in walls:
        return True, []
    # Hit a box?
    if (nr,nc) in boxes:
        moveable.append((nr,nc))
        # If this is part 1 or we're moving sideways then do this
        if boxes[(nr,nc)] == 'O' or dr == 0:
            blocked, _moveable = get_moveable(m, (nr,nc))
            if blocked: return True, []
            moveable.extend(_moveable)
        # If we're going up or down then we need to check for 2 spaces above us or not
        elif boxes[(nr,nc)] == '[':
            # Add the partner half of the box to the movable list
            moveable.append((nr,nc+1))
            for _nc in [nc, nc+1]:
                blocked, _moveable = get_moveable(m, (nr,_nc))
                if blocked: return True, []
                moveable.extend(_moveable)
        elif boxes[(nr,nc)] == ']':
            # Add the partner half of the box to the movable list
            moveable.append((nr,nc-1))
            for _nc in [nc, nc-1]:
                blocked, _moveable = get_moveable(m, (nr,_nc))
                if blocked: return True, []
                moveable.extend(_moveable)

    # We can move
    return False, moveable

def move(m,loc):
    global boxes
    lr,lc = loc
    blocked, moveable = get_moveable(m,loc)
    if blocked: return loc
    # Move the movable boxes
    dr,dc = m
    old_boxes = defaultdict()
    new_boxes = defaultdict()
    for tr,tc in moveable:
        old_boxes[(tr,tc)] = boxes[(tr,tc)]
        new_boxes[(tr+dr,tc+dc)] = boxes[(tr,tc)]
    for b in old_boxes.keys(): del boxes[b]
    for b in new_boxes.keys(): boxes[b] = new_boxes[b]
    # Also move the robot
    return (lr+dr,lc+dc)

def print_grid(m, loc):
    print('\nMove {}:'.format(m))
    for r in range(R):
        l = ''
        for c in range(C):
            if   (r,c) in walls: l += '#'
            elif (r,c) in boxes: l += boxes[(r,c)]
            elif (r,c) == loc: l += '@'
            else: l += '.'
        print(l)

for m in moves:
    nloc = move(MOVES[m],loc)
    loc = nloc

total = sum([r*100 + c for r,c in boxes])
print('Part 1:', total)

# -- Part 2 --

# Read everything in again

walls = set()
boxes = defaultdict()
moves = ''
loc = None

R = 0
C = 0

for r,line in enumerate(lines):
    if not line: continue
    if line.startswith('#'):
        R = r
        for c,char in enumerate(line):
            _c = c*2
            C = _c+1
            if char == '#':
                walls.add((r,_c))
                walls.add((r,_c+1))
            elif char == 'O':
                boxes[(r,_c)] = '['
                boxes[(r,_c+1)] = ']'
            elif char == '@':
                loc = (r,_c)
    else:
        moves += line

R += 1
C += 1

for m in moves:
    nloc = move(MOVES[m],loc)
    loc = nloc

total = sum([r*100 + c for r,c in boxes if boxes[(r,c)] == '['])
print('Part 2:', total)
