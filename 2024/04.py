grid = open("04.in").read().splitlines()

max_r = len(grid)-1
max_c = len(grid[0])-1

string = 'XMAS'

paths = []

def get_moves(loc,char,d=None):
    l = []
    r,c = loc
    if d is None:
        for dr,dc in [(0,1),(1,0),(0,-1),(-1,0),(-1,-1),(-1,1),(1,1),(1,-1)]:
            nr,nc = (r+dr,c+dc)
            if 0<=nr<=max_r and 0<=nc<=max_c and grid[nr][nc] is char:
                l.append(((nr,nc),(dr,dc)))
    else: # Already got a direction
        nr,nc = (r+d[0],c+d[1])
        if 0<=nr<=max_r and 0<=nc<=max_c and grid[nr][nc] is char:
            l.append(((nr,nc),d))
    return l

# Need a depth-first search recursion
def dfs(loc, char=0, d=None, p=[]):
    global string
    global paths
    total = 0
    r,c = loc
    # If this character is an S then we've found the end of a string
    if grid[r][c] == string[-1]:
        # End of the path but only from M
        paths.append(p)
        return 1
    # Get possible moves for matching
    moves = get_moves(loc,string[char+1],d)
    for move in moves:
        loc,_d = move
        # Move to the next square
        t = dfs(loc,char+1,_d,p+[loc])
        total += t
    return total

# Traverse the grid starting at each point and look for XMAS
total = 0
for r in range(max_r+1):
    for c in range(max_c+1):
        if grid[r][c] == string[0]:
            words = dfs((r,c), 0, None, [(r,c)])
            total += words

print('Part 1:', total)

# Part 2

# Find all the A's
total = 0
for r in range(1,max_r):
    for c in range(1,max_c):
        if grid[r][c] == 'A':
            # Check for crosses of MAS
            if (((grid[r-1][c-1] == 'M' and grid[r+1][c+1] == 'S') or
                 (grid[r-1][c-1] == 'S' and grid[r+1][c+1] == 'M')) and
                ((grid[r+1][c-1] == 'M' and grid[r-1][c+1] == 'S') or
                 (grid[r+1][c-1] == 'S' and grid[r-1][c+1] == 'M'))): total += 1

print('Part 2:', total)
