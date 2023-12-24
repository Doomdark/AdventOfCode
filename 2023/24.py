import re
import numpy.linalg as la
import z3

lines = open('24.in').read().splitlines()

class Hail:
    def __init__(self,num,px,py,pz,vx,vy,vz):
        self.px,self.py,self.pz,self.vx,self.vy,self.vz = px,py,pz,vx,vy,vz
        self.num = num

    def move(self, steps):
        px = self.px + (self.vx * steps)
        py = self.py + (self.vy * steps)
        pz = self.pz + (self.vz * steps)
        return Hail(self.num,px,py,pz,self.vx,self.vy,self.vz)

    # Solution from https://github.com/AllanTaylor314/AdventOfCode/blob/main/2023/24.py
    # Uses numpy linear algebra to solve the equation of 2 lines intersecting.
    # I wouldn't have thought of using that but it works.
    def intersect2d(self, other, start, end):
        try:
            # Make a matrix for numpy to solve
            t1, t2 = la.solve( [[self.vx,-other.vx], [self.vy,-other.vy]], [other.px-self.px,other.py-self.py])
        except la.LinAlgError:
            print(f"Failed to intersect {self} and {other}")
        else:
            if t1<0 or t2<0:
                return 0 # In the past
            # Returns the intersection point
            x = self.px+t1*self.vx
            y = self.py+t1*self.vy
            # Check that the intersect points are within the start/end bounds
            return all([start<=a<=end for a in [x,y]])
        return 0 # Parallel lines

    def __repr__(self):
        pos = ', '.join([str(x) for x in [self.px,self.py,self.pz]])
        vel = ', '.join([str(x) for x in [self.vx,self.vy,self.vz]])
        return ' @ '.join([pos,vel])

stones = []

for num,line in enumerate(lines):
    px,py,pz,vx,vy,vz = [int(x) for x in re.findall('[-\d]+', line)]
    stone = Hail(num,px,py,pz,vx,vy,vz)
    stones.append(stone)

def part1(start=7, end=27):
    intersections = 0
    done = set()
    for stonea in stones:
        for stoneb in stones:
            if stonea == stoneb: continue
            h = str(sorted([stonea.num, stoneb.num]))
            if h in done: continue
            done.add(h)
            intersections += stonea.intersect2d(stoneb, start, end)
    print('Part 1:', intersections)

part1(200000000000000, 400000000000000)

# Part 2

# z3 solution from the same place as the intersect above.

# Number of stones to give to the solver. 3 is the minimum required to get the right answer. Triangulation, see.
N = 3

# Make z3 integers x,y,z,u,v,w
x,y,z,u,v,w = map(z3.Int, "xyzuvw")

# Make times t0-tN for the first N stones
ts = [z3.Int("t{}".format(i)) for i in range(len(stones[:N]))]

# Make a solver instance
s = z3.Solver()

# Add the first 3 stones and times to the solver
for t, s in zip(ts, stones[:N]):
    # Add each dimension's constraint equation for this stone.
    # (predicted) position + (time * (predicted) velocity) == (known) position + (time * (known) velocity)
    s.add(x+t*u == s.px+t*s.vx)
    s.add(y+t*v == s.py+t*s.vy)
    s.add(z+t*w == s.pz+t*s.vz)

# Solve the constraints
s.check()

# Get the results
m = s.model()

# Sum the results of the x,y,z coordinates of the initial position of the rock
answer = sum(m[c].as_long() for c in (x,y,z))

print('Part 2:', answer)
