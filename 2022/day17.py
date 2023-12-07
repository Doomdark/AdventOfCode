class Rock:
    def __init__(self, shape):
        self.shape = shape

    def move_right(self, loc, obstructions):
        ok = True
        (lx,ly) = loc
        for x,y in self.shape:
            nx = lx+x+1
            ny = ly+y
            if (nx,ny) in obstructions:
                ok = False
            if nx == 7:
                ok = False
        if ok: return (lx+1,ly)
        else:  return (lx,ly)

    def move_left(self, loc, obstructions):
        ok = True
        (lx,ly) = loc
        for x,y in self.shape:
            nx = lx+x-1
            ny = ly+y
            if (nx,ny) in obstructions:
                ok = False
            if nx < 0:
                ok = False
        if ok: return (lx-1,ly)
        else:  return (lx,ly)

    def drop(self, loc, obstructions):
        ok = True
        (lx,ly) = loc
        for x,y in self.shape:
            nx = lx+x
            ny = ly+y-1
            if (nx,ny) in obstructions:
                ok = False
            if ny < 0:
                ok = False
        if ok: return (True,lx,ly-1)
        else:  return (False,lx,ly)

    def get_settled(self, loc):
        lx,ly = loc
        locs = {(lx+x,ly+y) for x,y in self.shape}
        return locs

from collections import defaultdict

# Rock shapes
minus  = Rock({(0,0),(1,0),(2,0),(3,0)})
cross  = Rock({(1,0),(0,1),(1,1),(2,1),(1,2)})
backl  = Rock({(0,0),(1,0),(2,0),(2,1),(2,2)})
pipe   = Rock({(0,0),(0,1),(0,2),(0,3)})
square = Rock({(0,0),(1,0),(0,1),(1,1)})

# Make a rocks list
rocks = []
rocks.append(minus)
rocks.append(cross)
rocks.append(backl)
rocks.append(pipe)
rocks.append(square)

verbose = False

def draw(settled):
    max_y = max([y for x,y in settled])
    print('---------------------')
    for y in range(max_y,-1,-1):
        row = ''
        for x in range(7):
            if (x,y) in settled:
                row += '#'
            else:
                row += '.'
        print(row)
    print()

def drop_rock(settled, highest=0, jets_index=0, rocks_index=0):
    # State checked - move the rock now
    moved = True
    # Get the next rock
    rock = rocks[rocks_index]
    # Place the rock first. What's the new rock offset?
    x,y = 2,3+(highest+1 if settled else 0)
    # While the rock is moving, update the location
    while moved:
        if verbose: draw(settled.union(rock.get_settled((x,y))))

        # Next x and y start with the current values
        nx,ny = x,y

        # Move the rock using the gas jets
        if jets[jets_index] == '>':
            nx,ny = rock.move_right((x,y),settled)
        else:
            nx,ny = rock.move_left((x,y),settled)

        if verbose: draw(settled.union(rock.get_settled((nx,ny))))

        # Try to drop the rock 1 unit
        moved,x,y = rock.drop((nx,ny),settled)

        # Next jet
        jets_index = (jets_index + 1) % len(jets)

    # Rock has stopped moving downwards. Add the rock shape to the settled locations list.
    final_rock_loc = rock.get_settled((x,y))
    settled.update(final_rock_loc)

    # Next rock
    rocks_index = (rocks_index + 1) % len(rocks)

    return (settled, rocks_index, jets_index)

# Drop the specified number of rocks
def drop_rocks(count):
    # Store the states of the rocks at the start of each drop
    states = defaultdict(set)
    # Store the highest of any of the columns
    highest = 0
    # Highest columns
    highest_ys=[0]*7
    # Rocks that have come to rest
    settled = set()
    # Which jet to use
    jets_index = 0
    # Which rock to use
    rocks_index = 0
    # Do the rocks now
    for i in range(count):

        # To work out the state, look at the skyline of the rocks
        highest = max(highest_ys)

        # Sum the normalised highest columns
        peak_sum = tuple(highest - p for p in highest_ys)

        # The peak_sum should be the same for the same jet and rock values for the state to be equivalent
        state_key = (rocks_index,jets_index,peak_sum)

        # If the state is in the states list then we've been here before...
        if state_key in states:
            (prev_i, prev_highest) = states[state_key]
            period = i - prev_i
            # How many period multiple are left?
            remaining_cycles = (count-i)//period
            # And how many additional rock drops are required after that?
            remaining_iterations = count - (i + period * remaining_cycles)
            # Extra to add to allow for the repeated periods
            x = (highest - prev_highest) * remaining_cycles
            # Do the rest of the rock drop iterations here now that we know how many there are
            for _ in range(remaining_iterations):
                (settled, rocks_index, jets_index) = drop_rock(jets_index=jets_index,
                                                               settled=settled, rocks_index=rocks_index,
                                                               highest=highest)

                # Update the highest column values
                for rx,ry in settled:
                    highest_ys[rx] = max(highest_ys[rx], ry)

                # Return the highest column
                highest = max(highest_ys)

            # Return the height from the other iterations plus the repats value plus 1 for the floor starting at -1
            return x+highest+1

        else: # New state
            states[state_key] = (i, highest)

        # Drop the rock
        (settled, rocks_index, jets_index) = drop_rock(settled, highest, jets_index, rocks_index)

        # Update the highest column values
        for rx,ry in settled:
            highest_ys[rx] = max(highest_ys[rx], ry)

        # Return the highest column
        highest = max(highest_ys)

    # Return the highest value plus 1 because the floor started at -1
    return (highest+1)

# Read jets
jets = [x for x in open("17.in").read().strip()]

# Initial repeat value
(height) = drop_rocks(2022)

print("Part 1:",height)

## Part 2 ##

rock_count = 1000000000000
(height) = drop_rocks(rock_count)

print("Part 2:",height)
