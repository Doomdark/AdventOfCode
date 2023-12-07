from intcode import Intcode
import threading

program = []

with open("day11_input.txt",'r') as f:
    for line in f.readlines():
        program = [int(x) for x in line.rstrip().split(',')]

p = []
for i in range(100000):
    p.append(0)
a = 0
for i in program:
    p[a] = i
    a += 1

class Computer(Intcode, threading.Thread):
    def __init__(self, program):
        threading.Thread.__init__(self)
        Intcode.__init__(self, program)

    def run(self):
        Intcode.run(self)

    def get(self):
        return self.output_queue.get()

    def put(self, value):
        c.input_queue.put(value)

# Start the computer
c = Computer(p)
c.start()

# Part 1

# Make a turn map
turn_map = {"U": {0:"L", 1:"R"},
            "D": {0:"R", 1:"L"},
            "L": {0:"D", 1:"U"},
            "R": {0:"U", 1:"D"}};

col_map = {0:'.', 1:'#'}

# Define how to move
def move(direction, x, y):
    import copy
    _x, _y = copy.deepcopy(x), copy.deepcopy(y)
    if   direction == "U": _y += 1
    elif direction == "D": _y -= 1
    elif direction == "L": _x -= 1
    elif direction == "R": _x += 1
    return _x, _y

def paint(col):
    # Initial condition
    x = 0
    y = 0
    coord     = (x,y)
    direction = "U"
    colour    = col

    # Store the initial position and colour
    colours   = {}
    painted_coords = []

    # Initialise the start panel
    colours[coord] = colour

    while 1:
        # Indicate the colour of the current panel
        if colours.has_key(coord):
            _col = colours[coord]
        else: # Haven't got this one. Assume it's black.
            _col = 0

        # Add the colour to the input queue
        c.put(_col)

        # Get the new colour and next direction from the output queue
        colour = c.get()
        turn   = c.get()

        # Paint the current location
        painted_coords.append(coord)

        # Store the new colour we painted it
        colours[coord] = colour

        # Change direction and move
        direction = turn_map[direction][turn]
        x, y = move(direction, x, y)

        # Update to the new coord
        coord = (x,y)

        # Exit if we're done
        if c._exit:
            break

    return colours

def draw_grid(colours):
    # Get grid extents
    max_x = max([x for x,y in colours.keys()])
    min_x = min([x for x,y in colours.keys()])
    max_y = max([y for x,y in colours.keys()])
    min_y = min([y for x,y in colours.keys()])

    # Print the grid
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            coord = (x,y)
            if colours.has_key(coord):
                print col_map[colours[coord]],
            else:
                print '.',
        print

colours = paint(0)
print "Part 1:", len(colours)
draw_grid(colours)

# Exit the computer thread
c.join()

# Part 2

# Re-initialise the computer
c = Computer(p)
c.start()

# Work out the max/min extents of the grid to draw
colours = paint(1)

print "Part 2:"
draw_grid(colours)

# Exit the computer thread
c.join()
