lines = []

# Read the input
with open("day02_input.txt") as f:
    for line in f.readlines():
        lines.append(line.strip())

# Part 1 start position
loc = (1,1)

# Possible moves
moves = {'U':(0,1),
         'D':(0,-1),
         'L':(-1,0),
         'R':(1,0)}

# Keypad number positions
numbers = {(0,2): "1",
           (1,2): "2",
           (2,2): "3",
           (0,1): "4",
           (1,1): "5",
           (2,1): "6",
           (0,0): "7",
           (1,0): "8",
           (2,0): "9"}

# Valid positions
valids = set(numbers.keys())

# Move to another key
def move(d, loc):
    global valids
    x,y = loc
    dx,dy = moves[d]
    nx = x+dx
    ny = y+dy
    if (nx,ny) not in valids: return loc
    return (nx,ny)

# Initialise the code
code = ""

for line in lines:
    for char in line:
        loc = move(char,loc)
    code += (numbers[loc])

print("Part 1:", code)

numbers = {(2,0): 'D',
           (1,1): 'A',
           (2,1): 'B',
           (3,1): 'C',
           (0,2): '5',
           (1,2): '6',
           (2,2): '7',
           (3,2): '8',
           (4,2): '9',
           (1,3): '2',
           (2,3): '3',
           (3,3): '4',
           (2,4): '1'}

# Valid positions
valids = set(numbers.keys())

# Start at '5' again
loc = (0,2)

# Initialise the code again
code = ""

for line in lines:
    for char in line:
        loc = move(char,loc)
    code += (numbers[loc])

print("Part 2:", code)
