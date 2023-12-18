from collections import defaultdict
from heapq import heappush, heappop

lines = open('17.in').read().splitlines()

grid = {}

max_r, max_c = 0,0

# Read input
for r,line in enumerate(lines):
    for c,char in enumerate(line):
        grid[(r,c)] = int(char)
        max_c = max(max_c,c)
    max_r = max(max_r,r)

size_r, size_c = max_r+1, max_c+1

DIRS        = {'e':(0,1), 's':(1,0), 'n':(-1,0), 'w':(0,-1)}
left_turns  = {'e':'n', 'n':'w', 'w':'s', 's':'e'}
right_turns = {'w':'n', 's':'w', 'e':'s', 'n':'e'}

def get_moves(d, loc, part2, steps):
    l = []
    r,c = loc
    left = left_turns[d]
    right = right_turns[d]
    straight = d
    # Default directions
    dirs = [left, right, straight]
    # Direction restrictions
    if part2:
        # Only go straight if count is <4
        if   steps  <  4: dirs = [straight]
        # Only go left/right if count is 10
        elif steps == 10: dirs = [left, right]
    else: # part 1
        # Only go left/right if count is 3
        if   steps ==  3: dirs = [left, right]
    # Next moves
    for new_dir in dirs:
        dr,dc = DIRS[new_dir]
        nr,nc = r+dr,c+dc
        if (nr,nc) in grid:
            l.append(((nr,nc), new_dir))
    return l

def print_path(p):
    for r in range(size_r):
        row = ''
        for c in range(size_c):
            if (r,c) in p: row += '#'
            else: row += '.'
        print(row)

def solve(part2=False):
    # Visited locations dict with minimum total heat loss
    visited = defaultdict(lambda: 999999)
    step_count = 0
    total = 0
    # Start position
    loc = (0,0)
    # Store states
    states = []
    # Mimimum heat loss
    minimum_loss = 999999
    # Final path for debug
    final_path = []
    
    # Starting position/directions. For part 2 we could start off going south, not east.
    for dir in ['s','e']:
        # Store the lowest total for this location
        visited[(loc, dir, 0)] = total
        # States to track movements
        state = (loc, dir, step_count, total, [loc])
        heappush(states, state)
    
    # Process all the states
    while states:
        # Current state
        loc, dir, step_count, total, path = heappop(states)
        # Are we at the end square now?
        if loc == (max_r,max_c):
            # Step count must be >= 4 for part 2
            if part2 and step_count < 4:
                continue
            if total < minimum_loss:
                minimum_loss = total
                final_path = path
            continue
        # Where can we go next?
        moves = get_moves(dir, loc, part2, step_count)
        # Check each move
        for move in moves:
            new_loc, new_dir = move
            # Make the new step count
            new_step_count = 1 if new_dir != dir else step_count + 1
            # Add on the new block's heat loss
            new_total = total + grid[new_loc]
            # Track the path for debug
            new_path = path[:]
            new_path.append(new_loc)
            # Been here before with a lower total?
            if new_total >= visited[(new_loc, new_dir, new_step_count)]:
                continue
            visited[(new_loc, new_dir, new_step_count)] = new_total
            # Otherwise add the new state to the queue
            new_state = (new_loc, new_dir, new_step_count, new_total, new_path)
            # Add the new state to the list
            heappush(states, new_state)

    #print_path(final_path)
    
    return minimum_loss

print('Part 1:', solve())

# Part 2

print('Part 2:', solve(True))

