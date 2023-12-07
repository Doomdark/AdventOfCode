from collections import deque
import math

lines = open("24.in").read().splitlines()

# There are 4 blizzard directions
blizzards = tuple(set() for i in range(4))
bchars = '<>^v'

for row,line in enumerate(lines[1:]):
    for col,char in enumerate(line[1:]):
        # Blizzard number assignments
        if char in bchars:
            blizzards[bchars.find(char)].add((row,col))

R = row
C = col

start = (-1,0)
end   = (R,C-1)
routes = [(start,end),(end,start),(start,end)]

def draw_grid(loc,time):
    print(time,loc,'-'*10)
    for r in range(0,R+1):
        row = ''
        for c in range(0,C+1):
            # Blizzard offset
            br,bc = (r - time)%R, (c - time)%C
            if   (r,c) == loc: row += 'E'
            elif (br,bc) in blizzards[bchars.find('^')]: row += '^'
            elif (br,bc) in blizzards[bchars.find('v')]: row += 'v'
            elif (br,bc) in blizzards[bchars.find('>')]: row += '>'
            elif (br,bc) in blizzards[bchars.find('<')]: row += '<'
            else: row += '.'
        print(row)

#draw_grid((-1,0),0)

# Start state for route 0
queue = deque([(0,-1,0,0)])

# Set to hold previously seen states
seen = set()

# Least common multiple of the grid size row and columns. This is how often the blizzards repeat.
lcm = R * C // math.gcd(R, C)

part1_done = False

# Keep going until we reach the end, or run out of states
while queue:
    # Get the state off the queue
    time,r,c,route = queue.popleft()

    # Next minute
    time += 1

    # Try all possible destinations
    for dr,dc in [(0,1),(0,-1),(1,0),(-1,0),(0,0)]:
        nr,nc = r+dr,c+dc

        # This is the current new route
        nroute = route

        # Have we reached the end of this route? The endpoints are off the grid so check for them first.
        if (nr,nc) == routes[route][1]:
            # Route 0 gives the answer for part 1
            if route == 0 and not part1_done:
                print('Part 1:',time)
                part1_done = True
            # Route 2 bies the answer for part 2
            elif route == 2:
                print('Part 2:',time)
                exit(0)
            # Update the route to switch to the next one
            nroute += 1

        # Check for out-of-grid accesses that aren't any of the route start or end points
        if (nr>=R or nr<0 or nc>=C or nc<0) and not (nr,nc) in [start,end]:
            continue

        # Are we in a blizzard if we move to this destination?
        in_blizzard = False

        # Only test against blizzards if we're not at either the start or the end
        if (nr,nc) not in [start,end]:
            # Test against all the blizzards. The blizzards move in time so add on the appropriate offset.
            #                     left    right     up      down
            for num, tr, tc in [(0,0,-1),(1,0,1),(2,-1,0),(3,1,0)]:
                # The blizzards wrap after R or C. Multiply the offset by the time and modulo max row/col counts.
                # Subtract the blizzard offset because they're moving.
                if ((nr - tr*time)%R, (nc - tc*time)%C) in blizzards[num]:
                    # Hit one of the 4 blizzards so we can't move this way
                    in_blizzard = True
                    break

        # Missed all the blizzards - add a new location if we haven't been there at exactly this blizzard condition already
        if not in_blizzard:
            # Make a key to check if we've been to this state before.
            seen_key = (nr,nc,nroute,time % lcm)
            if seen_key in seen:
                continue
            seen.add(seen_key)
            # Add the new state to the queue
            queue.append((time, nr, nc, nroute))
