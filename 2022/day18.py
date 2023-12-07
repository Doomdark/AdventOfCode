lines = open("18.in").read().splitlines()

cubes = set()

for line in lines:
    x,y,z = [int(x) for x in line.split(',')]
    cubes.add((x,y,z))

## Part 1 ##

# Find the number of surfaces which have no adjacents

nsurfaces = 0

def get_surfaces(cube):
    surfaces = 0
    # This cube
    x,y,z = cube
    # For each surface, try to match an adjacent cube
    for dx,dy,dz in [(0,0,1),(0,0,-1),(0,1,0),(0,-1,0),(1,0,0),(-1,0,0)]:
        # Adjacent cube to check against
        ccube = (x+dx,y+dy,z+dz)
        # If the cube being checked isn't in the list then this cube has that as a free surface
        if ccube not in cubes:
            surfaces += 1
    return surfaces

for cube in cubes:
   nsurfaces += get_surfaces(cube)

print("Part 1:", nsurfaces)

# This is the total surface area of all cubes.

## Part 2 ##

# Find the unreachable cubes inside the structure.

# Iterate across the grid finding the max and mins for each x,y,z.
minx,maxx = 1000,0
miny,maxy = 1000,0
minz,maxz = 1000,0

# Find the limits of the cube structure
for cube in cubes:
    x,y,z = cube
    minx,maxx = min(x,minx),max(x,maxx)
    miny,maxy = min(y,miny),max(y,maxy)
    minz,maxz = min(z,minz),max(z,maxz)

# Count the number of interior cubes
interior = 0

# Iterate over the maximum extents
for x in range(minx,maxx+1):
    for y in range(miny,maxy+1):
        for z in range(minz,maxz+1):
            # Test location maximums in x,y,z direction
            _minx,_maxx = 1000,0
            _miny,_maxy = 1000,0
            _minz,_maxz = 1000,0
            # Cube being tested
            ccube = (x,y,z)
            # Find the max extents of this x,y,z location by looking at each existing cube
            for cube in cubes:
                cx,cy,cz = cube
                # Check ccube is inside the cube structure
                if y == cy and z == cz: _minx,_maxx = min(cx,_minx),max(cx,_maxx)
                if x == cx and z == cz: _miny,_maxy = min(cy,_miny),max(cy,_maxy)
                if x == cx and y == cy: _minz,_maxz = min(cz,_minz),max(cz,_maxz)
            # Is the cube inside the structure boundary?
            if not (_minx<=x<=_maxx and _miny<=y<=_maxy and _minz<=z<=_maxz):
                continue
            # If the cube isn't in the list of cubes then it's free
            if ccube not in cubes:
                # How many free surfaces does this cube have?
                free_surfaces = get_surfaces(ccube)
                # Add on the number of non-free surfaces as that's part of the interior surface
                interior += 6-free_surfaces

print("Part 2:", nsurfaces - interior)
