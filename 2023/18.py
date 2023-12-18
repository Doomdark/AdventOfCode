lines = open('18.in').read().splitlines()

# Learned something new about maths today

def shoelace(area, corners):
    '''
    Shoelace theorem for finding internal areas of polygons.
    See https://artofproblemsolving.com/wiki/index.php/Shoelace_Theorem.
    '''
    # Iterate through each corner pair
    for i in range(len(corners)-1):
        # Next corner pair
        (x1,y1), (x2,y2) = corners[i:i+2]
        # Do the per-pair maths
        area += x1*y2 - x2*y1
    # Absolute area divided by 2 for the answer
    area = abs(area)//2
    return area

def pick(area, boundary):
    """
    Pick's theorem for finding the area of a polygon.
    See https://en.wikipedia.org/wiki/Pick%27s_theorem.
    This uses the area *inside* the polygon *plus* the length of its boundary points.
    So you need the internal polygon area, given by the Shoelace theorem, plus Pick's
    theorem to get the total polygon area for this puzzle.
    """
    return area + boundary//2 + 1
    
# Start location
loc = (0,0)
corners = [loc]
boundary = 0

def process_line(loc, dir, val, colour):
    global corners, boundary
    r,c = loc
    if   dir == 'R': nloc = (r, c+val)
    elif dir == 'D': nloc = (r+val, c)
    elif dir == 'L': nloc = (r, c-val)
    elif dir == 'U': nloc = (r-val, c)
    
    # Add new corner
    corners.append(nloc)
    # Add the boundary length
    boundary += val
    # Return new location
    return nloc

def solve():
    global loc, corners, boundary
    
    # Read input
    for line in lines:
        dir, val, col = line.split(' ')
        loc = process_line(loc, dir, int(val), col)

    # Shoelace theorem
    area = shoelace(0, corners)
    # Pick's theorem
    area = pick(area, boundary)
    
    return area

print('Part 1:', solve())

# Part 2

DIRS = {'0':'R', '1':'D', '2':'L', '3':'U'}
    
# Start location
loc = (0,0)
corners  = [loc]
boundary = 0

# Update the process_line function for part 2
def process_line(loc, dir, val, colour):
    global corners, boundary
    r,c = loc
    dir = DIRS[colour[-2]]
    val = int(colour[2:-2],16)
    
    if   dir == 'R': nloc = (r, c+val)
    elif dir == 'D': nloc = (r+val, c)
    elif dir == 'L': nloc = (r, c-val)
    elif dir == 'U': nloc = (r-val, c)

    # Add new corner
    corners.append(nloc)
    # Add the boundary length
    boundary += val
    # Return new location
    return nloc

print('Part 2:', solve())
