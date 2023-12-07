import re

extractor = re.compile(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%.*')

nodes = {}

max_x = 0

with open('22.in') as f:
    for line in f.readlines():
        match = extractor.match(line)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            size = int(match.group(3))
            used = int(match.group(4))
            avail = int(match.group(5))
            use = int(match.group(6))
            max_x = max(max_x,x)
            nodes[(x,y)] = {'size':size,
                           'used':used,
                           'avail':avail,
                           'use':use}
viable = 0

for nodea, valsa in nodes.items():
    for nodeb, valsb in nodes.items():
        if nodea == nodeb: continue\
        if valsa['used'] == 0: continue
        if valsa['used'] > valsb['avail']: continue
        viable += 1

print('Part 1:', viable)

# Part 2

def get_adjacents(loc):
    x,y = loc
    adjs = {}
    for dx,dy in [(0,-1), (0,1), (-1,0), (1,0)]:
        nx,ny = x+dx,y+dy
        if (nx,ny) in nodes:
            adjs[(nx,ny)] = nodes[(nx,ny)]
    return adjs

from collections import deque

def solve():
    steps = 0
    loc = (max_x,0)
    
