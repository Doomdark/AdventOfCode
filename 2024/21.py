from collections import defaultdict, deque

codes = open('21.in').read().splitlines()

# Make the numeric keypad
n = ['789','456','123','.0A']
nR,nC = 4,3
N = {}

# Make the direction keypad
d = ['.^A', '<v>']
dR,dC = 2,3
D = {}

def md(a,b):
    'Manhattan distance'
    return abs(b[0]-a[0]) + abs(b[1]-a[1])

def paths(grid,r,c,R,C):
    'Find all the shortest paths to the other squares on the provided grid starting from (r,c).'
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
            # Get the Manhattan distance between the two points
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

# Get all shortest distances from each key to each other key
for r,line in enumerate(n):
    for c,char in enumerate(line):
        if n[r][c] != '.':
            N[char] = paths(n,r,c,nR,nC)

# Get all shortest distances from each key to each other key
for r,line in enumerate(d):
    for c,char in enumerate(line):
        if d[r][c] != '.':
            D[char] = paths(d,r,c,dR,dC)

# OK, now we have all the possible shortest routes from everywhere to everywhere else

# Do a DFS function which recursively determines the shortest set of button presses starting from keypad N and digit M (posn)

# Cache the results
DP = {}

def dfs(DEPTH, CHAR, POSN='A'):
    # Return a value from the cache if there's an appropriate entry
    if (DEPTH,CHAR,POSN) in DP:
        return DP[(DEPTH,CHAR,POSN)]
    # Which keypad for this depth?
    keypad = keypads[DEPTH]
    # Paths to get to CHAR from POSN
    paths = keypad[POSN][CHAR]
    # If we're last in the keypad chain then choose path 0 from the list as they're all the same length
    if DEPTH+1 == len(keypads):
        # Store the length in the cache
        DP[(DEPTH,CHAR,POSN)] = len(paths[0])
        return len(paths[0])
    # OK, now try to figure out the shortest path from here to the end. Start with a chunky shortest path length.
    shortest = 10**12
    # Iterate over the shortest paths in the list for this keypad
    for path in paths:
        # Zero length to start with for each path
        current = 0
        # We always start at A
        posn = 'A'
        # A path looks something like this: ^v<A
        for char in path:
            # Recurse to the next keypad in the chain
            current += dfs(DEPTH+1, char, posn)
            # Continue from the previous char
            posn = char
        # Is the current path shorter than the current shortest?
        shortest = min(shortest,current)
    # Store the shortest length in the cache
    DP[(DEPTH,CHAR,POSN)] = shortest
    # Return the shortest length
    return shortest

# Determine the "complexity" of the code
def get_complexity(paths):
    total = 0
    for c,p in zip(codes,paths):
        _c = int(c.lstrip('0').rstrip('A'))
        total += _c * p
    return total

# -- Run --

# The last set of directions is in the last pad so we don't need it
for part,pads in [(1,2),(2,25)]:
    # Make a list of pads to traverse
    keypads = [N] + [D] * pads
    # Clear the cache
    DP = {}
    # List of shortest path lengths for each code
    PATHS = []
    # Test each code
    for code in codes:
        PATH = 0
        # Start at A
        posn = 'A'
        # Find the shortest path length for each char. The next search starts from the previous one.
        for char in code:
            PATH += dfs(0, char, posn)
            posn = char
        PATHS.append(PATH)

    print(f'Part {part}:', get_complexity(PATHS))
