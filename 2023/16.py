lines = open('16.in').read().splitlines()

# Stores for mirrors and splitters
mirrors = {}
splitters = {}
# Stores for current beams and visited places
beams = []
lit = set()
beam_visited = set()
# Directions
dirs = {'e':(0,1), 'w':(0,-1), 's':(1,0), 'n':(-1,0)}
# Max grid dimensions
max_r, max_c = 0, 0

# Read input
for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if char in '\/':
            mirrors[(r,c)] = char
        elif char in '-|':
            splitters[(r,c)] = char
        max_c = max(max_c,c)
    max_r = max(max_r,r)

size_r, size_c = max_r+1, max_c+1

def print_grid():
    for r in range(size_r):
        row = ''
        for c in range(size_c):
            if (r,c) in mirrors: row += mirrors[(r,c)]
            elif (r,c) in splitters: row += splitters[(r,c)]
            else: row += '.'
        print(row)

def print_lit():
    for r in range(size_r):
        row = ''
        for c in range(size_c):
            if (r,c) in lit: row += '#'
            else: row += '.'
        print(row)

# Beam class
class Beam:
    def __init__(self, loc, dir):
        self.dir = dir
        self.loc = loc
        self.stop = False
        
    def inside_grid(self):
        r,c = self.loc
        return 0<=r<=max_r and 0<=c<=max_c

    def move(self):
        r,c = self.loc
        dr,dc = dirs[self.dir]
        nr,nc = r+dr,c+dc
        self.loc = (nr,nc)

    def turn_and_move(self):
        # Check if a beam has been here before
        beam_check = (self.loc, self.dir)
        if beam_check in beam_visited:
            self.stop = True
            return
        beam_visited.add(beam_check)
        
        # Are we on a mirror square?
        if self.loc in mirrors:
            self.dir = turn(self.dir, mirrors[self.loc])
            self.move()
        # Are we on a splitter square?
        elif self.loc in splitters:
            newdirs = split(self.dir, splitters[self.loc])
            # Did we split?
            if len(newdirs) > 1:
                # Make a new beam with the new direction
                beam = Beam(self.loc, newdirs[1])
                # Add it to the list of beams
                beams.append(beam)
            # Now move this beam
            self.dir = newdirs[0]
            self.move()
        else:
            self.move()

# Resulting turn direction
def turn(d, mirror):
    if   d == 'e': return 'n' if mirror == '/' else 's'
    elif d == 's': return 'w' if mirror == '/' else 'e'
    elif d == 'w': return 's' if mirror == '/' else 'n'
    elif d == 'n': return 'e' if mirror == '/' else 'w'

# Resulting beam split
def split(d, splitter):
    if splitter == '-': return d if d in 'we' else 'we'
    else:               return d if d in 'sn' else 'sn'

# Solve the puzzle
def solve(LOC, DIR):
    global beams, lit, beam_visited

    # Clear the lists and sets
    beams = []
    lit = set()
    beam_visited = set()

    # Start location and direction
    beam = Beam(LOC, DIR)
    beams.append(beam)
    lit.add(LOC)

    # Allow the beam to propagate
    timeout_count = max(max_r,max_c)
    count = 0

    # Whilst there are beams remaining
    while beams:
        new_beams = []
        lit_count = len(lit)
        # Move the beam(s)
        for beam in beams:
            beam.turn_and_move()
        # Check all the beams now they've all moved
        for beam in beams:
            # If  the beam is inside the grid extents then add its location to the lit set
            if beam.inside_grid():
                lit.add(beam.loc)
                # If we haven't been here before then carry on
                if not beam.stop:
                    new_beams.append(beam)
        # Have we lit any new squares since last iteration?
        if len(lit) == lit_count:
            count += 1
            if count == timeout_count:
                break
        else:
            count = 0
        # Current beams
        beams = list(set(new_beams))

    return len(lit)

# Start location and direction for part 1
LOC = (0,0)
DIR = 'e'

print('Part 1:', solve(LOC, DIR))

# Part 2

def part2():
    max_energy = 0

    # All east points
    for r in range(size_r):
        max_energy = max(max_energy, solve((r,0), 'e'))
    # All west points
    for r in range(size_r):
        max_energy = max(max_energy, solve((r,max_c), 'w'))
    # All south points
    for c in range(size_c):
        max_energy = max(max_energy, solve((0,c), 's'))
    # All north points
    for c in range(size_c):
        max_energy = max(max_energy, solve((max_r,c), 'n'))

    return max_energy

print('Part 2:', part2())
