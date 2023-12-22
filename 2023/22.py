import re, operator, copy

lines = open('22.in').read().splitlines()

class Brick:
    def __init__(self, name, loc):
        self.name = name
        self.points = set()
        self.moved = False
        fx,fy,fz,sx,sy,sz = [int(x) for x in re.findall('\d+', loc)]
        for x in range(fx,sx+1):
            for y in range(fy,sy+1):
                for z in range(fz,sz+1):
                    self.points.add((x,y,z))

    def get_lowest_point(self):
        return (min([z for x,y,z in self.points]), self)

    def drop(self, bricks, update=True):
        # Check if any other bricks would be in the way if we dropped 1->n squares
        if any([z==1 for x,y,z in self.points]):
            return False
        # Make a set of all the current occupied points other than for this brick
        all_points = set()
        for brick in bricks:
            if brick == self: continue
            all_points.update(brick.points)
        # If any of the brick's points are at a height of 1 then that's as low as it can get already
        dz = 0
        while True:
            npoints = set()
            # New points
            for p in self.points:
                npoints.add((p[0],p[1],p[2]-1))
            # Now check for collisions against all other bricks
            if npoints & all_points:
                break
            # No collision - update this brick's points
            self.points = npoints
            dz += 1
            # Can't drop any further than z==1
            if any([z==1 for x,y,z in self.points]):
                break
        if update:
            self.moved = dz>0

    def __repr__(self):
        return ', '.join([str(x) for x in sorted(self.points)])

bricks = []

# Process the bricks
for i, line in enumerate(lines):
    brick = Brick(i, line)
    bricks.append(brick)

def drop_all_bricks(bricks, update=False):
    # Drop the bricks until they stop
    lowest_first = sorted([x.get_lowest_point() for x in bricks], key=operator.itemgetter(0))
    for height, brick in lowest_first:
        brick.drop(bricks, update)

    return bricks

# Initial drop
bricks = drop_all_bricks(bricks, False)

# All the bricks have dropped. Try to remove each one and see if they would cause any others bricks to drop
safe = 0
total_drop = 0
for ibrick in bricks:
    drop_count = 0
    # Make a brick set without the brick in that we're testing
    _bricks = set()
    # Make a new set of bricks to test against without the brick we've removed
    for brick in bricks:
        if brick == ibrick: continue
        # Copy yhe original brick to preserve its state
        _bricks.add(copy.deepcopy(brick))
    # Drop all the bricks for this combination
    _bricks = drop_all_bricks(_bricks, True)
    # Check the moved flag in each brick
    moved = sum([b.moved for b in _bricks])
    # At least one brick moved
    if moved:
        drop_count += 1
        # Sum the number of bricks that moved in total
        total_drop += moved
    # If drop count is 0 then it was safe to remove this brick
    if drop_count == 0:
        safe += 1

print('Part 1:', safe)
print('Part 2:', total_drop)
