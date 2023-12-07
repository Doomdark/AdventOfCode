lines = open('14.in').read().splitlines()

reindeer = []

class Reindeer:
    def __init__(self, name, speed, time, rest):
        self.name = name
        self.speed = speed
        self.time = time
        self.rest = rest
        self.state = 'move'
        self.count = 0
        self.distance = 0
        self.points = 0

    def update(self):
        if self.state == 'move':
            self.distance += self.speed
            self.count += 1
            if self.count == self.time:
                self.state = 'rest'
                self.count = 0
        else:
            self.count += 1
            if self.count == self.rest:
                self.state = 'move'
                self.count = 0

for line in lines:
    l = line.split()
    name = l[0]
    speed = int(l[3])
    time = int(l[6])
    rest = int(l[13])
    r = Reindeer(name, speed, time, rest)
    reindeer.append(r)

for i in range(2503):
    for r in reindeer:
        r.update()
    # Get the furthest distance of all the reindeer
    furthest = max([x.distance for x in reindeer])
    # Add a point to te furthest
    for r in reindeer:
        if r.distance == furthest:
            r.points += 1

max_dist   = max([x.distance for x in reindeer])
max_points = max([x.points for x in reindeer])

print('Part 1:', max_dist)
print('Part 2:', max_points)
