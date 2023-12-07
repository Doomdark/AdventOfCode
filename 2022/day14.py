walls = set()
sand  = set()
source = (500,0)

# Read the input
lines = open("14.in").read().splitlines()

for line in lines:
    corners = line.strip().split(' -> ')
    # Iterate through the corners
    for c in range(len(corners)-1):
        start = corners[c]
        end   = corners[c+1]
        sx,sy = [int(x) for x in start.split(',')]
        ex,ey = [int(x) for x in end.split(',')]
        # Swap the x,y start/end if end is less than start
        if ex < sx: sx,ex = ex,sx
        if ey < sy: sy,ey = ey,sy
        # Add the walls
        for x in range(sx,ex+1):
            for y in range(sy,ey+1):
                walls.add((x,y))

# Grid size
min_x = 0
max_x = max([ x for x,y in walls ])+1
min_y = 0
max_y = max([ y for x,y in walls ])+1

# Grid printer guy
def print_grid(trim):
    trimmed_min_x = min([ x for x,y in walls.union(sand) ])-1
    trimmed_min_y = min([ y for x,y in walls.union(sand) ])-1
    trimmed_max_x = max([ x for x,y in walls.union(sand) ])+2
    trimmed_max_y = max([ y for x,y in walls.union(sand) ])+2

    _min_x = trimmed_min_x if trim else min_x
    _min_y = trimmed_min_y if trim else min_y
    _max_x = trimmed_max_x if trim else max_x
    _max_y = trimmed_max_y if trim else max_y

    for y in range(_min_y,_max_y):
        row = ''
        for x in range(_min_x,_max_x):
            if (x,y) in walls:
                row += '#'
            elif (x,y) in sand:
                row += 'o'
            elif (x,y) == source:
                row += '+'
            elif (x,y) == cur:
                row += '+'
            else:
                row += '.'
        print(row)
    print()

# Move the sand
def move(cur,part2=False):
    x,y = cur
    # Try to move down in order
    for nx,ny in [(x,y+1), (x-1,y+1), (x+1,y+1)]:
        # Is the new point on the grid?
        # If we're on part 2 then ignore the x min and max values
        if (part2 or (nx >= min_x and nx < max_x)) and ny >= min_y and ny < max_y:
            # Is the new point not a wall or existing sand?
            if (nx,ny) not in walls and (nx,ny) not in sand:
                return (True,nx,ny,False)
        else:
            # Only say it's offgrid if this isn't part 2
            return(False,x,y,not part2)
    # Couldn't move
    return (False,x,y,False)

# Set the current point to be the source
cur = source

while True:
    # New sand
    moved, nx, ny, offgrid = move(cur)
    # Did the sand move that time?
    if offgrid:
        break
    elif not moved:
        # Nope, add it to the sand set
        sand.add((nx,ny))
        # If we didn't move and the current position is the source then we're full
        if (nx,ny) == source:
            break
        # Make a new bit of sand to move
        cur = source
    else:
        cur = (nx,ny)

print_grid(True)

print('Part 1:', len(sand))

## Part 2 ##

# The floor got futher away
max_y += 1

# Reset some thing
sand = set()
cur = (500,0)

while True:
    # New sand
    moved, nx, ny, offgrid = move(cur,True)
    # Did the sand move that time?
    if not moved:
        # Nope, add it to the sand set
        sand.add((nx,ny))
        # If we didn't move and the current position is the source then we're full
        if (nx,ny) == source:
            break
        # Make a new bit of sand to move
        cur = source
    else:
        cur = (nx,ny)

print('Part 2:', len(sand))
