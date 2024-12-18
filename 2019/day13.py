import copy
from intcode import Intcode
from collections import defaultdict

program = defaultdict(int)

with open("day13_input.txt",'r') as f:
    for line in f.readlines():
        for i,x in enumerate(line.rstrip().split(',')):
            program[i] = int(x)

tile_map = {0:' ', # Empty
            1:'#', # Wall
            2:'=', # Block
            3:'-', # Paddle
            4:'o'} # Ball

joystick = { 0:'+',
            -1:'<',
             1:'>'}

##### Part 1
####def draw():
####    # Start the computer
####    c = Intcode(program)
####    c.start()
####
####    coords = {}
####    while 1:
####        if c.running:
####            x = c.get()
####            y = c.get()
####            t = c.get()
####            coord = (x,y)
####
####            # Check what was in the current coordinate.
####            # If a ball hits a block then it's destroyed.
####            coords[coord] = t
####
####        else:
####            if c._exit:
####                return sum([(value == 2) for value in coords.itervalues()])
####
####blocks_remaining = draw()
####
####print "Part 1:", blocks_remaining

# Part 2

def draw_screen(coords):
    max_x = 0
    max_y = 0

    for x,y in coords.keys():
        if x > max_x: max_x = x
        if y > max_y: max_y = y

    print(max_x, max_y)

    for y in range(max_y+1):
        row = ''
        for x in range(max_x+1):
            coord = (x,y)
            if coords.has_key(coord):
                row += tile_map[coords[coord]]
            else:
                row += '.'
        print(row)
    print()


# Part 2

def play():
    # Start the computer
    d = Intcode(program)

    # Add 2 quarters by setting memory address 0 to 2
    d.memory[0] = 2

    # Start the computer
    d.start()

    coords = {}
    score = 0
    loop = 0

    # Paddle moving
    paddle_x = None
    ball_x   = None
    joystick_move = 0

    blocks_left = 9999

    while 1:

        # The game updates the paddle/ball by blanking the current ball in one frame and then adding it again in the next frame.
        # Move the joystick if the ball moves.

        # Get the new tile values. Every iteration has a tile output.
        x = d.get()
        y = d.get()
        t = d.get()

        # Score appears when x == -1
        if x == -1 and y == 0:
            score = t

        else: # Otherwise it's a new coord
            coord = (x,y)

            # Check what was in the current coordinate.
            # If a ball hits a block then it's destroyed.
            coords[coord] = t

            if t == 3: paddle_x = x
            if t == 4: ball_x   = x

            # Where should the paddle go next?
            if   ball_x > paddle_x: joystick_move =  1
            elif ball_x < paddle_x: joystick_move = -1
            else:                   joystick_move =  0

        # Not every iteration needs an input... How do I get round that?

        #if paddle_x is not None and ball_x is not None:
        d.put(joystick_move)

        print("-- Loop {} - Score = {} - B,P = ({},{}) - Joystick moving {} --".format(loop, score, ball_x, paddle_x, joystick[joystick_move]))
        draw_screen(coords)

        # Any blocks left?
        #blocks_left = sum([(value == 2) for value in coords.itervalues()])
        #print "({}) Blocks left:".format(loop), blocks_left

        loop += 1

        # if d._exit:
        #     print "Exited"
        #     d.join()
        #     return score

score = play()
print("Part 2:", score)
