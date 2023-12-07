import re, itertools, copy, math
number  = "([-]*\d+)"

# Make a class to store each moon's info
class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def update_velocity(self, m):
        if   m.x > self.x: self.vx += 1
        elif m.x < self.x: self.vx -= 1
        if   m.y > self.y: self.vy += 1
        elif m.y < self.y: self.vy -= 1
        if   m.z > self.z: self.vz += 1
        elif m.z < self.z: self.vz -= 1

    def axis_data(self, axis):
        if axis == "X": return self.x, self.vx
        if axis == "Y": return self.y, self.vy
        if axis == "Z": return self.z, self.vz

    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def __repr__(self):
        return "pos=<x={:>3}, y={:>3}, z={:>3}>, vel=<x={:>3}, y={:>3}, z={:>3}>".format(self.x,self.y,self.z, self.vx, self.vy, self.vz)

    def potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def kinetic_energy(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    def energy(self):
        return self.potential_energy() * self.kinetic_energy()

    def key(self):
        return [str(self.x), str(self.y), str(self.z), str(self.vx), str(self.vy), str(self.vz)]

class Moons:
    def __init__(self, input_file):
        self.moons = []

        with open(input_file,'r') as f:
            for line in f.readlines():
                match = re.match("^<x={n},\s+y={n},\s+z={n}>".format(n=number), line)
                if match:
                    x = int(match.group(1))
                    y = int(match.group(2))
                    z = int(match.group(3))
                    self.moons.append(Moon(x, y, z))

    def update(self):
        for moon in self.moons:
            for other_moon in self.moons:
                moon.update_velocity(other_moon)

        for moon in self.moons:
            moon.update_position()

    def total_energy(self):
        return sum([x.energy() for x in self.moons])

    def __repr__(self):
        result = [str(x) for x in self.moons]
        return '\n'.join(result).strip()

    def repeats_per_axis(self, axis):
        steps = 0
        previous = {}
        pos1, vel1 = self.moons[0].axis_data(axis)
        pos2, vel2 = self.moons[1].axis_data(axis)
        pos3, vel3 = self.moons[2].axis_data(axis)
        pos4, vel4 = self.moons[3].axis_data(axis)
        found = False

        # Run until we've got the repeat for this axis
        while not found:
            if pos1 in previous:
                if vel1 in previous[pos1]:
                    if pos2 in previous[pos1][vel1]:
                        if vel2 in previous[pos1][vel1][pos2]:
                            if pos3 in previous[pos1][vel1][pos2][vel2]:
                                if vel3 in previous[pos1][vel1][pos2][vel2][pos3]:
                                    if pos4 in previous[pos1][vel1][pos2][vel2][pos3][vel3]:
                                        if vel4 in previous[pos1][vel1][pos2][vel2][pos3][vel3][pos4]:
                                            return steps
                                        else:
                                            previous[pos1][vel1][pos2][vel2][pos3][vel3][pos4].append(vel4)
                                    else:
                                        previous[pos1][vel1][pos2][vel2][pos3][vel3][pos4] = [vel4]
                                else:
                                    previous[pos1][vel1][pos2][vel2][pos3][vel3] = {}
                                    previous[pos1][vel1][pos2][vel2][pos3][vel3][pos4] = [vel4]
                            else:
                                previous[pos1][vel1][pos2][vel2][pos3] = {}
                                previous[pos1][vel1][pos2][vel2][pos3][vel3] = {}
                                previous[pos1][vel1][pos2][vel2][pos3][vel3][pos4] = [vel4]
                        else:
                            previous[pos1][vel1][pos2][vel2] = {}
                            previous[pos1][vel1][pos2][vel2][pos3] = {}
                            previous[pos1][vel1][pos2][vel2][pos3][vel3] = {}
                            previous[pos1][vel1][pos2][vel2][pos3][vel3][pos4] = [vel4]
                    else:
                        previous[pos1][vel1][pos2] = {}
                        previous[pos1][vel1][pos2][vel2] = {}
                        previous[pos1][vel1][pos2][vel2][pos3] = {}
                        previous[pos1][vel1][pos2][vel2][pos3][vel3] = {}
                        previous[pos1][vel1][pos2][vel2][pos3][vel3][pos4] = [vel4]
                else:
                    previous[pos1][vel1] = {}
                    previous[pos1][vel1][pos2] = {}
                    previous[pos1][vel1][pos2][vel2] = {}
                    previous[pos1][vel1][pos2][vel2][pos3] = {}
                    previous[pos1][vel1][pos2][vel2][pos3][vel3] = {}
                    previous[pos1][vel1][pos2][vel2][pos3][vel3][pos4] = [vel4]
            else:
                previous[pos1] = {}
                previous[pos1][vel1] = {}
                previous[pos1][vel1][pos2] = {}
                previous[pos1][vel1][pos2][vel2] = {}
                previous[pos1][vel1][pos2][vel2][pos3] = {}
                previous[pos1][vel1][pos2][vel2][pos3][vel3] = {}
                previous[pos1][vel1][pos2][vel2][pos3][vel3][pos4] = [vel4]

            # Update the moons
            self.update()

            # Get the new values from each moon
            pos1, vel1 = self.moons[0].axis_data(axis)
            pos2, vel2 = self.moons[1].axis_data(axis)
            pos3, vel3 = self.moons[2].axis_data(axis)
            pos4, vel4 = self.moons[3].axis_data(axis)

            # Next step
            steps += 1
        return steps

# Read in the input file

Example  = Moons("day12_example.txt")
Example2 = Moons("day12_example2.txt")
Part1    = Moons("day12_input.txt")

for i in range(10):
    Example.update()
print( "Example 1: Total Energy =", Example.total_energy() )

for i in range(100):
    Example2.update()
print( "Example 2: Total Energy =", Example2.total_energy() )

for i in range(1000):
    Part1.update()
print( "Part 1: Total Energy =", Part1.total_energy() )

# Part 2

# For each axis determine the number of iterations until it repeats
def find_axis_repeats(input_file):
    # Initialise the list each time to find the repeat from zero

    # X first
    moons = Moons(input_file)
    x_repeat = moons.repeats_per_axis("X")
    print('X axis repeats at', x_repeat )

    # Y
    moons = Moons(input_file)
    y_repeat = moons.repeats_per_axis("Y")
    print('Y axis repeats at', y_repeat )

    # Z
    moons = Moons(input_file)
    z_repeat = moons.repeats_per_axis("Z")
    print('Z axis repeats at', z_repeat )

    # Multiply the repeats together and divide by the greatest common divisor to find the minimum repeat
    lowest_common_multiple_xy = (x_repeat * y_repeat) // math.gcd(x_repeat, y_repeat)
    lowest_common_multiple    = (lowest_common_multiple_xy * z_repeat) // math.gcd(lowest_common_multiple_xy, z_repeat)
    return lowest_common_multiple

print( "Example 1 steps until repeat:", find_axis_repeats('day12_example.txt') )
print( "Example 2 steps until repeat:", find_axis_repeats('day12_example2.txt') )
print( "Part 2 steps until repeat:",    find_axis_repeats('day12_input.txt') )
