grid = open("04test2.in").read().splitlines()

max_r = len(grid)-1
max_c = len(grid[0])-1

string = 'XMAS'

def get_moves(loc,char,d=None,path=[]):
    l = []
    r,c = loc
    if d is None:
        for dr,dc in [(0,1),(1,0),(0,-1),(-1,0),(-1,-1),(-1,1),(1,1),(1,-1)]:
            nr,nc = (r+dr,c+dc)
            if 0<=nr<=max_r and 0<=nc<=max_c and grid[nr][nc] is char:
                p = path[:]
                p.append((nr,nc))
                l.append(((nr,nc),(dr,dc),p))
    else: # Already got a direction
        nr,nc = (r+d[0],c+d[1])
        if 0<=nr<=max_r and 0<=nc<=max_c and grid[nr][nc] is char:
            p = path[:]
            p.append((nr,nc))
            l.append(((nr,nc),d,p))
    return l

# Need a depth-first search recursion
def dfs(loc, char=0, d=None,p=[]):
    global string
    total = 0
    r,c = loc
    # If this character is an S then we've found the end of a string
    if grid[r][c] == string[-1]:
        return 1,[p]
    # Get possible moves for matching
    moves = get_moves(loc,string[char+1],d,p)
    for move in moves:
        loc,_d,p = move
        #if move not in visited:
        t,path = dfs(loc,char+1,_d,p)
        total += t
        if path is not None:
            p.extend(path)
    return total,p

# Traverse the grid starting at each point and look for XMAS
total = 0
for r in range(max_r+1):
    for c in range(max_c+1):
        if grid[r][c] == string[0]:
            words = dfs((r,c), 0, None, [])
            total += words[0]

print('Part 1:', total)

string = "MAS"

for r in range(max_r+1):
    for c in range(max_c+1):
        if grid[r][c] == string[0]:
            words = dfs((r,c), 0, None, [])
print(paths)
