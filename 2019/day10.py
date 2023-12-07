import math, operator

asteroids = []

def manhattan_dist(origin, target):
    return abs(origin[0]-target[0]) + abs(origin[1]-target[1])

def angle(origin, target):
    ox, oy = origin
    tx, ty = target
    # The grid is negative in the Y direction for atan2 so swap origin[y] and target[y]
    a = math.atan2(tx-ox, oy-ty)
    # Compensate for pi/-pi returned by atan2 by adding 2pi for negative numbers
    if a < 0.0:
        a += 2*math.pi
    return a

class Asteroid:
    def __init__(self, x, y):
        self.coord = (x, y)
        self.x = x
        self.y = y
        self.angle  = 0.0
        self.dist   = 0
        self.others = []

    def get_others (self, asteroids):
        for b in asteroids:
            # Skip ourselves
            if self == b: continue
            _angle = angle(self.coord, b.coord)
            _dist  = manhattan_dist(self.coord, b.coord)
            c = Asteroid(b.x, b.y)
            c.angle = _angle
            c.dist = _dist
            self.others.append(c)

    def get_visible_count (self):
        # Get a list of the unique different angles of the other asteroids
        all_angles = set([x.angle for x in self.others])
        self.visible_count = len(all_angles)
        return self.visible_count

    def vaporize(self):
        count = 0
        while count < 200:
            # Get all the asteroids again with with the y axis flipped
            visible = self.get_visible_ordered()
            # Remove each of the objects in this list from the list of self.others
            for a in visible:
                count += 1
                if count == 200:
                    return a
                self.others.remove(a)

    # Monitoring station laser
    def get_visible_ordered (self):
        # Store the angles in a dictionary
        angles = {}

        # Find the nearest asteroid for each angle
        for a in self.others:
            if not angles.has_key(a.angle):
                angles[a.angle] = a
            elif angles[a.angle].dist > a.dist:
                angles[a.angle] = a

        # Sort the angles of all the asteroids to be in rotation order starting from 0.0 radians
        nearest = sorted([y for x,y in sorted(angles.iteritems())], key=operator.attrgetter('angle'))

        return nearest

x, y = 0, 0

with open("day10_input.txt",'r') as f:
    for line in f.readlines():
        for p in line:
            if p == '#':
                a = Asteroid(x, y)
                asteroids.append(a)
            x += 1
        x = 0
        y += 1

# Check each asteroid against the other asteroids for visibility
for a in asteroids:
    a.get_others(asteroids)

# Now work out the nearest visible asteroids
most_others_visible = asteroids[0]
for a in asteroids[1:]:
    if a.get_visible_count() > most_others_visible.get_visible_count():
        most_others_visible = a

print "Part 1:", most_others_visible.coord, most_others_visible.visible_count

# The laser monitoring station is on the asteroid which has the most visible other asteroids.
z = most_others_visible.vaporize()
print "Part 2:", z.x*100 + z.y
