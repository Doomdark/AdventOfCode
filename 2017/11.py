curr = (0,0)

moves = {'n' : (0,+1),
         'ne': (+0.5, +0.5),
         'se': (+0.5, -0.5),
         's' : (0,-1),
         'sw': (-0.5,-0.5),
         'nw': (-0.5,+0.5)
         }

def hex_manhattan_distance(loc):
    'Assuming we start from 0,0'
    x,y = loc
    return abs(x) + abs(y)

steps = open('11.in').read().rstrip().split(',')

furthest = 0

for step in steps:
    dx,dy = moves[step]
    x,y = curr
    nx,ny = x+dx,y+dy
    curr = (nx,ny)
    furthest = max(hex_manhattan_distance(curr),furthest)

print('Part 1:', hex_manhattan_distance(curr))
print('Part 2:', furthest)
