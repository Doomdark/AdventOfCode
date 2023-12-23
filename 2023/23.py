from collections import deque

grid = open('23.in').read().splitlines()
start = (0,1)
end   = (len(grid)-1, len(grid[0])-2)

def get_adjacents(loc, part2=False):
    r,c = loc
    # Possible neighbours
    # If the location is immediately north of the exit then that can be the only route.
    # Otherwise the exit will be blocked and the rest of the path is pointless.
    if (r,c+1) == end:
        yield (r, c+1)
        return
    for dr,dc in [(0,1),(0,-1),(1,0),(-1,0)]:
        nr,nc = r+dr,c+dc
        # Check for on-grid
        if 0<=nr<len(grid) and 0<=nc<len(grid[0]):
            # Part 1 has <>^v as slopes where you must go in that direction if the current square says to
            if not part2:
                # Check for slopes
                if grid[r][c] in '<>^v':
                    # Do the slope thing
                    if   grid[r][c] in '>' and dc ==  1: yield (nr,nc)
                    elif grid[r][c] in '<' and dc == -1: yield (nr,nc)
                    elif grid[r][c] in 'v' and dr ==  1: yield (nr,nc)
                    elif grid[r][c] in '^' and dr == -1: yield (nr,nc)
                # Not a slope, check for not a wall in the next square
                elif grid[nr][nc] != '#':
                    yield (nr,nc)
            else: # Part 2 treats slopes as normal squares so just check for walls in the next square
                if grid[nr][nc] != '#':
                    yield (nr,nc)

def make_graph(grid, part2=False):
    # Make a normal graph of the grid
    G = {}
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            # Connected squares
            if grid[r][c] != '#':
                # Add all the edges for this location with a weight of 1
                G[(r,c)] = [(1,n) for n in get_adjacents((r,c), part2)]
    return G

# Make a graph of the grid
G = make_graph(grid)

# Solve the puzzle with a breadth-first search
def bfs(G):
    visited = set()
    visited.add(start)
    queue = deque()
    queue.append((start, 0, visited))
    max_steps = 0

    while queue:
        loc, steps, visited = queue.pop()
        r,c = loc
        # Reached the end?
        if r == len(grid)-1:
            max_steps = max(max_steps, steps)
        # Iterate through the moves in the graph
        for d, move in G[loc]:
            # If we've not already been here then go
            if move not in visited:
                nvisited = visited.copy()
                nvisited.add(move)
                queue.append((move, steps+d, nvisited))
    return max_steps

print('Part 1:', bfs(G))

# Part 2

def collapse_path(G, current, head):
    count = 1
    # Whilst there are only 2 destinations from the current square in the grid then it's a straight line
    while len(G[head]) == 2:
        count += 1
        # Get the next destination if it isn't the current location
        tail = [dest for l,dest in G[head] if dest != current][0]
        # Update the current position along the path
        current, head = (head, tail)
    # Return the end of the path and how far it was
    return (count, head)

def make_compressed_graph(G):
    # Collapse all continuous steps into a single step
    cG = {}
    # For each destination merge the multiple steps into a single step of length n
    for src, dests in G.items():
        cG[src] = [collapse_path(G, src, dest) for l,dest in dests]
    return cG

G = make_graph(grid, True)
cG = make_compressed_graph(G)

print('Part 2:', bfs(cG))
