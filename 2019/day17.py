from intcode import Intcode
from collections import defaultdict

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
            c += 1
            if a == 35:
                scaffold.add((r,c))
    else:
        MAXR = max([r for r,c in scaffold])
        MAXC = max([c for r,c in scaffold])
        MINR = min([r for r,c in scaffold])
        MINC = min([c for r,c in scaffold])
        #draw_grid()
        intersections = sum([(r-MINR)*(c-MINC) for r,c in scaffold if intersection(r,c)])
        print('Part 1:', intersections)
        break
