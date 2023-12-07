from hashlib import md5
from collections import deque

min_x, max_x = 0,3
min_y, max_y = 0,3

#passcode = 'hijkl'
#passcode = 'ihgpwlah'
#passcode = 'kglvqrro'
#passcode = 'ulqzkmiv'
passcode = 'gdjjyniy'

dirs = {(0,-1) : 'U',
        (0, 1) : 'D',
        (-1,0) : 'L',
        ( 1,0) : 'R'
        }

door_dir = [x for x in dirs.values()]

def get_adjacents(loc):
    x,y = loc
    adjs = {}
    for dx,dy in [(0,-1), (0,1), (-1,0), (1,0)]:
        nx,ny = x+dx,y+dy
        if min_x<=nx<=max_x and min_y<=ny<=max_y:
            adjs[dirs[(dx,dy)]] = (nx,ny)
    return adjs

def get_doors(path):
    src = passcode+path
    h = md5(src.encode()).hexdigest()[:4]
    open_doors = set()
    for door,hh in enumerate(h):
        if hh in ['b','c','d','e','f']:
            open_doors.add(door_dir[door])
    return open_doors

def solve(part1=True):
    path = ''
    loc = (0,0)
    q = deque()
    q.append((loc, path))
    max_path_len = 0
    
    while q:
        loc,path = q.popleft()
        open_doors = get_doors(path)
        adjacent_doors = get_adjacents(loc)
        for door,new_loc in adjacent_doors.items():
            if door in open_doors:
                new_path = path+door
                if new_loc == (max_x,max_y):
                    if part1:
                        return new_path
                    else:
                        max_path_len = max(max_path_len, len(new_path))
                else:
                    q.append((new_loc,new_path))

    return max_path_len
            
print('Part 1:', solve())
print('Part 2:', solve(False))
