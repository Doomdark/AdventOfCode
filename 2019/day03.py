import sys

def manhattan_distance(coords):
    return abs(coords[0]) + abs(coords[1])

collisions = []

class Wire:
    def __init__(self):
        self.location = (0,0)
        self.coords   = set()
        self.steps    = 0
        self.collision_step_counts = []

    def add_move(self, move, check_steps = False):
        # Extract the movement
        direction = move[0]
        amount    = int(move[1:])

        # Iterate through the moves, adding coordinates to the set
        for i in range(1, amount+1, 1):
            self.steps += 1
            if   direction == 'R': new_coord = (self.location[0]+i, self.location[1])
            elif direction == 'L': new_coord = (self.location[0]-i, self.location[1])
            elif direction == 'U': new_coord = (self.location[0],   self.location[1]+i)
            elif direction == 'D': new_coord = (self.location[0],   self.location[1]-i)

            self.coords.add(new_coord)

            # If we're checking the step count then see if this coord is one of the collisions
            if check_steps:
                if new_coord in collisions:
                    self.collision_step_counts.append((new_coord, self.steps))

        # Update our location
        if   direction == 'R': self.location = (self.location[0]+amount, self.location[1])
        elif direction == 'L': self.location = (self.location[0]-amount, self.location[1])
        elif direction == 'U': self.location = (self.location[0],        self.location[1]+amount)
        elif direction == 'D': self.location = (self.location[0],        self.location[1]-amount)

    def get_collisions(self, other):
        '''Get the location of the common coords using a set intersection'''
        myset      = self.coords
        otherset   = other.coords
        commonset  = myset.intersection(otherset)
        return list(commonset)

    def nearest_collision_to_zero(self, other):
        '''Work out the nearest collision to zero with the Manhattan distance'''
        collisions = self.get_collisions(other)

        nearest = 0xFFFFFFFF

        for c in collisions:
            dist = manhattan_distance(c)
            if dist < nearest:
                nearest = dist

        return nearest

# make a list to store the wires in
wires = []

# Read in the wires
with open("day03_input.txt","r") as f:
    for line in f.readlines():
        # Make a wire instance
        wire = Wire()
        # Split the input line
        moves = line.split(',')
        # Iterate over the moves
        for move in moves:
            wire.add_move(move)
        # Add the wire to the list
        wires.append(wire)

# Now compare the wires for nearest-to-zero collisions
print "Part 1: Nearest collision distance:", wires[0].nearest_collision_to_zero(wires[1])

# Now read in the input again and count the step count for each collision to be lazy
collisions = wires[0].get_collisions(wires[1])

# Reset the wires list
wires = []

with open("day03_input.txt","r") as f:
    for line in f.readlines():
        # Make a wire instance
        wire = Wire()
        # Split the input line
        moves = line.split(',')
        # Iterate over the moves
        for move in moves:
            wire.add_move(move, True)
        # Add the wire to the list
        wires.append(wire)

# Now check for step counts
shortest = 0xFFFFFFFF

# Iterate through the collisions
for w0_coord, w0_steps in wires[0].collision_step_counts:
    for w1_coord, w1_steps in wires[1].collision_step_counts:
        # Check the coords match
        if w0_coord == w1_coord:
            total = w0_steps + w1_steps
            if total < shortest:
                shortest = total

print "Part 2: Shortest collision step distance", shortest
