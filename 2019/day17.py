from intcode import Intcode
from collections import defaultdict, deque

# Program memory
program = defaultdict(int)
program.update({i:int(x) for i,x in enumerate(open("day17_input.txt").read().rstrip().split(','))})

# Run the computer
computer = Intcode(program)
computer.start()

l = ''
r,c = 0,0
scaffold = set()
MAXR,MAXC = 0,0
MINR,MINC = 0,0
start = (0,0)
robot = None

DIRS  = {'^':(-1,0), '<':(0,-1), 'v':(1,0), '>':(0,1)}
RDIRS = {(-1,0):'^', (0,-1):'<', (1,0):'v', (0,1):'>'}
LEFT  = {'^':'<', '<':'v', 'v':'>', '>':'^'}
RIGHT = {'^':'>', '<':'^', 'v':'<', '>':'v'}

def intersection(r,c):
    result = True
    for dr,dc in [(0,-1),(0,1),(1,0),(-1,0)]:
        nr,nc = r+dr,c+dc
        if (nr,nc) not in scaffold:
            return False
    return result

def draw_grid():
    for r in range(MINR,MAXR+1):
        l = ''
        for c in range(MINC,MAXC+1):
            #if (r,c) == start: l+=robot
            if (r,c) in scaffold: l += 'O' if intersection(r,c) else '#'
            else: l += '.'
        print(l)

while True:
    a = computer.get()
    if a is not None:
        if a == 10:
            r += 1
            c = 0
        else:
            if chr(a) in ['^','<','v','>']:
                start = (r,c)
                robot = chr(a)
            c += 1
            if a == 35:
                scaffold.add((r,c))
    else:
        MAXR = max([r for r,c in scaffold])
        MAXC = max([c for r,c in scaffold])
        MINR = min([r for r,c in scaffold])
        MINC = min([c for r,c in scaffold])
        draw_grid()
        intersections = sum([(r-MINR)*(c-MINC) for r,c in scaffold if intersection(r,c)])
        print('Part 1:', intersections)
        break

# -- Part 2 --

import copy

# Now we've got the scaffold and the robot start position, we can determine the route to take.
# It's basically to never turn unless it's a proper corner.

def adjacents(loc):
    r,c = loc
    adjacents = set()
    visited = set()
    for dr,dc in [(0,-1),(0,1),(1,0),(-1,0)]:
        nr,nc = r+dr,c+dc
        if (nr,nc) in scaffold and (nr,nc):
            if (nr,nc) in SEEN:
                visited.add((nr,nc))
            else:
                adjacents.add((nr,nc))
    return adjacents, visited

# Hold the required movements
paths = []
SEEN = set()

def bfs(loc, robot):
    global paths
    Q = deque()
    Q.append((0, loc, robot, set(), []))
    while Q:
        moves, (r,c), robot, SEEN, movements = Q.popleft()
        nSEEN = SEEN | {(r,c)}

        # Got to the end of the scaffolding length and have visited every square
        if moves >= len(scaffold):
            if SEEN - scaffold == set():
                paths.append(movements)
            continue

        # Try to move forward
        nr,nc = r+DIRS[robot][0], c+DIRS[robot][1]
        if (nr,nc) in scaffold and (nr,nc) not in nSEEN:
            nmovements = copy.copy(movements)
            Q.append((moves+1, (nr,nc), robot, nSEEN, nmovements))

        nr,nc = r+DIRS[LEFT[robot]][0], c+DIRS[LEFT[robot]][1]
        if (nr,nc) in scaffold and (nr,nc) not in nSEEN:
            nrobot = LEFT[robot]
            nmovements = copy.copy(movements)
            if moves>0:
                nmovements.append(moves)
            nmovements.append('L')
            Q.append((0, (r,c), nrobot, nSEEN, nmovements))

        nr,nc = r+DIRS[RIGHT[robot]][0], c+DIRS[RIGHT[robot]][1]
        if (nr,nc) in scaffold and (nr,nc) not in nSEEN:
            nrobot = RIGHT[robot]
            nmovements = copy.copy(movements)
            if moves>0:
                nmovements.append(moves)
            nmovements.append('R')
            Q.append((0, (r,c), nrobot, nSEEN, nmovements))

# Trace the robot's path so we can see the repeated turns and moves
bfs(start, robot)
print(len(paths))
#for movements in paths:
#    print(','.join([str(x) for x in movements]))
exit()
# So I get this as the movements:
# L,10,L,10,R,6,L,10,L,10,R,6,R,12,L,12,L,12,R,12,L,12,L,12,L,6,L,10,R,6
# L,9,L,10,R,6,L,10,L,10,R,6,R,12,L,12,L,12,R,12,L,12,L,12,L,6,L,10,R,6

#
L,9,L,10,R,6,
L,10,L,10,R,6,
R,12,L,12,L,12,
R,12,L,12,
L,12,L,6,L,10,
R,12,R,12,R,12,L,12,
L,12,L,6,L,10,
R,12,R,12,R,12,L,12,
L,12,L,6,L,10,
R,12,R,12,
L,10,L,10,R,6

# The repeats are:
# A: R,12,L,12,L,12
# B: L,10,L,10,R,6
# C: L,6,L,10,R,6
# But I'm not sure the code will understand multiple-digit numbers so do this instead:
# A: R,6,6,L,6,6,L,6,6
# B: L,5,5,L,5,5,R,6
# C: L,6,L,5,5,R,6
# And the pattern is:
# B,B,A,A,C

program = defaultdict(int)
program.update({i:int(x) for i,x in enumerate(open("day17_input.txt").read().rstrip().split(','))})

# Run the computer
computer = Intcode(program)
computer.memory[0] = 2
computer.start()

A = ['R','6','6','L','6','6','L','6','6']
B = ['L','5','5','L','5','5','R','6']
C = ['L','6','L','5','5','R','6']
P = ['B','B','A','A','C']

for a in P:
    computer.put(ord(a))
computer.put(ord('\n'))
print(computer.get())
for a in A:
    computer.put(ord(a))
computer.put(ord('\n'))
print(computer.get())
for a in B:
    computer.put(ord(a))
computer.put(ord('\n'))
print(computer.get())
for a in C:
    computer.put(ord(a))
computer.put(ord('\n'))
computer.put(ord('y'))
computer.put(ord('\n'))

while True:
    print(computer.get())
