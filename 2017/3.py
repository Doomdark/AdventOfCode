from collections import defaultdict

num = 347991

dirs = {'r':(0,1), 'l':(0,-1), 'u':(-1,0), 'd':(1,0)}

def md (a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def next_dir(d,loc,visited):
    r,c = loc
    nd = d
    # Try to always turn left compared to the current position
    if   d == 'r': nd = 'u'
    elif d == 'u': nd = 'l'
    elif d == 'l': nd = 'd'
    elif d == 'd': nd = 'r'
    dr,dc = dirs[nd]
    nloc = (r+dr,c+dc)
    # Can we go that way?
    if nloc in visited:
        return d
    else:
        return nd

count = 1
d = 'r'
loc = (0,0)
visited = set()
visited.add(loc)

while count < num:
    r,c = loc
    # Move
    dr,dc = dirs[d]
    nr,nc = r+dr,c+dc
    loc = (nr,nc)
    visited.add(loc)
    d = next_dir(d,loc,visited)
    count += 1
    #print (loc,count,d)

print('Part 1:',md((0,0),loc))

## Part 2 ##

def get_neighbours(loc,visited):
    r,c = loc
    neighbour_sum = 0
    for dr,dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        nloc = (r+dr,c+dc)
        if nloc in visited:
            neighbour_sum += visited[nloc]
    return neighbour_sum

d = 'r'
loc = (0,0)
visited = defaultdict(int)
visited[loc] = 1

while True:
    r,c = loc
    # Move
    dr,dc = dirs[d]
    nr,nc = r+dr,c+dc
    loc = (nr,nc)
    visited[loc] = get_neighbours(loc,visited)
    d = next_dir(d,loc,visited)
    if visited[loc] > num:
        break

print('Part 2:', visited[loc])
