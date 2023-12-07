import re
from collections import deque

spaces = set()
walls = set()

lines = open("22.in").read().splitlines()
route = None

directions = deque(['>','v','<','^'])
facing = {'>':0, 'v':1, '<':2, '^':3}

row = 0
for line in lines:
    if line.startswith('1'):
        r = re.findall(r'(\d+|\w)', line)
        route = []
        # Translate the distances into ints
        for item in r:
            try:
                i = int(item)
                route.append(i)
            except:
                route.append(item)
    else:
        for col,char in enumerate(line):
            if   char == '#': walls.add((row,col))
            elif char == '.': spaces.add((row,col))
        row += 1

grid = spaces.union(walls)

def turn(turning):
    if   turning == 'L': directions.rotate(1)
    elif turning == 'R': directions.rotate(-1)
    return directions[0]

def move(loc,d):
    global spaces
    global grid
    row,col = loc
    # Going right
    if   d == '>': nr,nc = row,col+1
    elif d == 'v': nr,nc = row+1,col
    elif d == '<': nr,nc = row,col-1
    elif d == '^': nr,nc = row-1,col
    # Space to move into
    if (nr,nc) in spaces: return (nr,nc)
    # If the new space isn't on the grid then wrap around
    if (nr,nc) not in grid:
        # Wrap around
        if   d == '>': nc = min([c for r,c in grid if r == nr])
        elif d == 'v': nr = min([r for r,c in grid if c == nc])
        elif d == '<': nc = max([c for r,c in grid if r == nr])
        elif d == '^': nr = max([r for r,c in grid if c == nc])
        # If the wrapped-around space is a wall then don't move
        if (nr,nc) in spaces: return (nr,nc)
    # Move is blocked
    return (row,col)

#print(route)

# Starting direction
direction = '>'
# Starting location
loc = (0,min(c for r,c in spaces if r == 0))

path = {}

def draw(grid):
    global path
    global spaces
    global walls
    print('-'*10)
    rmax = max(r for r,c in grid)
    for r in range(rmax+1):
        row = ''
        cmax = max(c for r,c in grid)
        for c in range(cmax+1):
            if   (r,c) in path  : row += path[(r,c)]
            elif (r,c) in spaces: row += '.'
            elif (r,c) in walls : row += '#'
            else: row += ' '
        print(row)

#draw(walls.union(spaces))

# Move along the route
for item in route:
    # Moving
    if isinstance(item, int):
        for m in range(item):
            path[loc] = direction
            loc = move(loc,direction)
            #print(item, 'Moving', direction,'to',loc)
    else:
        direction = turn(item)
        path[loc] = direction
        #print('Turning',item,'to face',direction)

#draw(walls.union(spaces))

fr,fc = loc
print('Part 1:', (1000*(fr+1)) + (4*(fc+1)) + facing[direction])

## Part 2 ##

### # Not a generic solution
### # For example input, faces are:
### # A = (0->3),(8->11)
### # B = (4->7),(0->3)
### # C = (4->7),(4->7)
### # D = (4->7),(8->11)
### # E = (8->11),(8->11)
### # F = (8->11),(12->15)
### #
### #   A
### # BCD
### #   EF
### #       CurFace  CurDir NFace,NDir
### facemove = {'A':   {'>':  ('F','<'),
###                     'v':  ('D','v'),
###                     '<':  ('C','v'),
###                     '^':  ('B','^')},
###             'B':   {'>':  ('C','>'),
###                     'v':  ('E','^'),
###                     '<':  ('F','^'),
###                     '^':  ('A','v')},
###             'C':   {'>':  ('D','>'),
###                     'v':  ('E','>'),
###                     '<':  ('B','<'),
###                     '^':  ('A','>')},
###             'D':   {'>':  ('F','v'),
###                     'v':  ('E','v'),
###                     '<':  ('C','<'),
###                     '^':  ('A','^')},
###             'E':   {'>':  ('F','>'),
###                     'v':  ('B','^'),
###                     '<':  ('C','^'),
###                     '^':  ('D','^')},
###             'F':   {'>':  ('A','<'),
###                     'v':  ('B','v'),
###                     '<':  ('E','<'),
###                     '^':  ('D','<')}
###             }
###
### faces = {}
###
### faces['A'] = [0,8]
### faces['B'] = [4,0]
### faces['C'] = [4,4]
### faces['D'] = [4,8]
### faces['E'] = [8,8]
### faces['F'] = [8,12]
###
### face_size = 4

# Not a generic solution
#
#   AB
#   C
#  DE
#  F

#         CurFace  CurDir NFace,NDir
facemove = {'A':   {'>':  ('B','>'),
                    'v':  ('C','v'),
                    '<':  ('D','>'),
                    '^':  ('F','>')},
            'B':   {'>':  ('E','<'),
                    'v':  ('C','<'),
                    '<':  ('A','<'),
                    '^':  ('F','^')},
            'C':   {'>':  ('B','^'),
                    'v':  ('E','v'),
                    '<':  ('D','v'),
                    '^':  ('A','^')},
            'D':   {'>':  ('E','>'),
                    'v':  ('F','v'),
                    '<':  ('A','>'),
                    '^':  ('C','>')},
            'E':   {'>':  ('B','<'),
                    'v':  ('F','<'),
                    '<':  ('D','<'),
                    '^':  ('C','^')},
            'F':   {'>':  ('E','^'),
                    'v':  ('B','v'),
                    '<':  ('A','v'),
                    '^':  ('D','^')}
            }

faces = {}

# Top-left corners of faces on grid
faces['A'] = [0,50]
faces['B'] = [0,100]
faces['C'] = [50,50]
faces['D'] = [100,0]
faces['E'] = [100,50]
faces['F'] = [150,0]

face_size = 50

face_max = face_size - 1

def cube_move(face,loc,d):
    global spaces
    global grid
    row,col = loc
    nface = face
    nd = d
    turns = []
    # Moving
    if   d == '>': nr,nc = row,col+1
    elif d == 'v': nr,nc = row+1,col
    elif d == '<': nr,nc = row,col-1
    elif d == '^': nr,nc = row-1,col
    # Space to move into
    if (nr,nc) in spaces:
        #print('A space')
        # update the face
        for f in faces:
            rmin,cmin = faces[f]
            rmax = rmin+face_max
            cmax = cmin+face_max
            if rmin<=nr<=rmax and cmin<=nc<=cmax:
                nface = f
                #print('New face',f,nr,nc,rmin,rmax,cmin,cmax)
                break
        return nface,turns,(nr,nc)
    # If the new space isn't on the grid then wrap around
    if (nr,nc) not in grid:
        # What's the new face?
        nface,nd = facemove[face][d]
        # We've changed direction
        if d == '>':
            if nd == 'v':
                roffset = 0
                coffset = face_max - (row % face_size)
                turns = ['R']
            elif nd == '<':
                roffset = face_max - (row % face_size)
                coffset = face_max
                turns = ['R','R']
            elif nd == '^':
                roffset = face_max
                coffset = (row % face_size)
                turns = ['L']
            else:
                roffset = (row % face_size)
                coffset = 0
        elif d == 'v':
            if nd == '^':
                roffset = face_max
                coffset = face_max - (col % face_size)
                turns = ['R','R']
            elif nd == '>':
                roffset = face_max - (col % face_size)
                coffset = 0
                turns = ['L']
            elif nd == '<':
                roffset = (col % face_size)
                coffset = face_max
                turns = ['R']
            else:
                roffset = 0
                coffset = (col % face_size)
        elif d == '<':
            if nd == '^':
                roffset = face_max
                coffset = face_max - (row % face_size)
                turns = ['R']
            elif nd == 'v':
                roffset = 0
                coffset = (row % face_size)
                turns = ['L']
            elif nd == '>':
                roffset = face_max - (row % face_size)
                coffset = 0
                turns = ['L','L']
            else:
                roffset = (row % face_size)
                coffset = face_max
        elif d == '^':
            if nd == '<':
                roffset = face_max - (col % face_size)
                coffset = face_max
                turns = ['L']
            elif nd == 'v':
                roffset = 0
                coffset = face_max - (col % face_size)
                turns = ['L','L']
            elif nd == '>':
                roffset = (col % face_size)
                coffset = 0
                turns = ['R']
            else:
                roffset = face_max
                coffset = (col % face_size)

        # New face's top-left corner
        minr,minc = faces[nface]
        # Apply the offsets to get the new location
        nr,nc = minr+roffset,minc+coffset

        # If the wrapped-around space is a wall then don't move
        if (nr,nc) in spaces:
            return nface,turns,(nr,nc)
        else: # Blocked
            nface = face
            turns = []
    # Move is blocked
    return nface,turns,(row,col)


# Starting direction
direction = '>'
# Starting location
loc = (0,min(c for r,c in spaces if r == 0))
# Starting cube face
face = 'A'

path = {}

# Move along the route
for item in route:
    # Moving
    if isinstance(item, int):
        for m in range(item):
            path[loc] = direction
            nface,turns,nloc = cube_move(face,loc,direction)
            ndirection = direction
            for t in turns:
                ndirection = turn(t)
            #print(item, 'Moving', direction,'from',face,loc,'to',nface,nloc,'ndir',ndirection)
            direction = ndirection
            face = nface
            loc = nloc
    else:
        direction = turn(item)
        path[loc] = direction
        #print('Turning',item,'to face',direction)

#draw(walls.union(spaces))

fr,fc = loc
#print(fr,fc,direction)
print('Part 2:', (1000*(fr+1)) + (4*(fc+1)) + facing[direction])
