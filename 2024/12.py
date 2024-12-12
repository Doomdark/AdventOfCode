lines = open('12test3.in').read().splitlines()

from collections import defaultdict
import sys
sys.setrecursionlimit(10*6)

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

def flood(AREA, name, r, c):
    global lines
    AREA.add((r,c))
    for dr,dc in [(0,1), (0,-1), (1,0), (-1,0)]:
        nr,nc = r+dr,c+dc
        if 0<nr<max_r and 0<nc<max_c:
            if lines[nr][nc] == name and (nr,nc) not in AREA:
                flood(AREA, name, nr, nc)

SEEN = set()
for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if (r,c) not in SEEN:
            AREA = set()
            flood(AREA, char, r, c)
            SEEN |= AREA
            if char == 'R':
                print(SEEN)
            regions[char].append(list(AREA))

print(regions['R'])

def get_perimeter(area):
    total = 0
    #print(area)
    for r,c in area:
        open_sides = 4-adjacent(area, r, c)
        total += open_sides
        #print('-',r, c, open_sides)
    return total

def get_area(area):
    return len(area)

total = 0
for name, area_list in regions.items():
    for area in area_list:
        #print(name, area)
        _area = get_area(area)
        _perimeter = get_perimeter(area)
        print(name, _area, _perimeter)
        total += _area * _perimeter

print('Part 1:', total)
