from collections import defaultdict, deque

codes = open('21.in').read().splitlines()

# Make the keypads
n = ['789','456','123','.0A']
nR,nC = 4,3
d = ['.^A', '<v>']
dR,dC = 2,3
N = {}
D = {}

def md(a,b):
    return abs(b[0]-a[0]) + abs(b[1]-a[1])

def paths(grid,r,c,R,C):
    Q = deque()
    Q.append((0,r,c,'',0))
    paths = {}
    SEEN = set()
    while Q:
        dist, cr, cc, path, lmd = Q.popleft()
        if (cr,cc,path) in SEEN: continue
        SEEN.add((cr,cc,path))
        char = grid[cr][cc]
        if char not in paths:
            paths[char] = defaultdict(list)
        # Add the path for the current char into the dictionary
        if path not in paths[char][len(path)]:
            paths[char][len(path)].append(path+'A')
        # Go to each other point
        for dr,dc,d in [(0,1,'>'),(0,-1,'<'),(1,0,'v'),(-1,0,'^')]:
            nr,nc = cr+dr,cc+dc
            MD = md((r,c),(nr,nc))
            # Use Manhattan distance to ensure we always move away from the source button
            if 0<=nr<R and 0<=nc<C and grid[nr][nc] != '.' and MD == lmd+1:
                Q.append((dist+1,nr,nc,path+d,MD))
    # Return a dictionary of all the shortest paths to each destination
    ans = {}
    for char,lens in paths.items():
        shortest = min(lens.keys())
        ans[char] = lens[shortest]
    return ans

# Get all possible routes from each point to each other point
for r,line in enumerate(n):
    for c,char in enumerate(line):
        if n[r][c] != '.':
            N[char] = paths(n,r,c,nR,nC)

# Get all possible routes from each point to each other point
for r,line in enumerate(d):
    for c,char in enumerate(line):
        if d[r][c] != '.':
            D[char] = paths(d,r,c,dR,dC)

# OK, now we have all the possible shortest routes from everywhere to everywhere else

# Do a DFS function which recursively determines the shortest set of button presses starting from keypad N and digit M (posn)

DP = {}
def dfs(depth, digit, posn='A'):
    # Return a value from the cache if there's an appropriate entry
    if (depth,digit,posn) in DP:
        return DP[(depth,digit,posn)]
    # Which keypad for this depth?
    keypad = keypads[depth]
    # Paths to get to that digit from A as we always start from A
    paths = keypad[posn][digit]
    # Is this the last keypad?
    last = depth+1 == len(keypads)
    # If we're last in the chain then choose path 0 from the list as it doesn't matter
    if last:
        DP[(depth,digit,posn)] = len(paths[0])
        return len(paths[0])
    # OK, now try to figure out the shortest path from here to the end
    PATH = 0
    shortest = None
    # Iterate over the shortest paths in the list
    for path in paths:
        # For this path we always start at A
        _path = 0
        POSN = 'A'
        # A path looks like this ^v<A
        for _digit in path:
            _path += dfs(depth+1, _digit, POSN)
            POSN =_digit
        if shortest is None or _path < shortest:
            shortest = _path
    # Store the shortest length in the cache
    DP[(depth,digit,posn)] = shortest
    # Return the shortest length
    return shortest

# Determine the "complexity" of the code
def get_complexity(paths):
    total = 0
    for c,p in zip(codes,paths):
        _c = int(c.lstrip('0').rstrip('A'))
        total += _c * p
    return total

# -- Part1 --

# Evaluate part 1 with a small number of keypads
keypads = [N,D,D]

total = 0
PATHS = []
for code in codes:
    PATH = 0
    posn = 'A'
    for digit in code:
        PATH += dfs(0, digit, posn)
        posn = digit
    PATHS.append(PATH)

print('Part 1:', get_complexity(PATHS))

# -- Part 2 --

# Evaluate part 1 with a chunky number of keypads
keypads = [N,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D]

# Reset the cache
DP = {}

# Evaluate
total = 0
PATHS = []
for code in codes:
    PATH = 0
    posn = 'A'
    for digit in code:
        PATH += dfs(0, digit, posn)
        posn = digit
    PATHS.append(PATH)

print('Part 2:', get_complexity(PATHS))
