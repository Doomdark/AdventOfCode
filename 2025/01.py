# This one is modulus arithmetic as everything wraps at 99, so modulo 100.

# Read the input
lines = open("01.in").read().splitlines()

# Set some variables
dial = 50
zeroes = 0

for line in lines:
    # How far does the dial move?
    num = int(line[1:])
    # Which direction?
    if line.startswith('L'):
        dial = (dial - num) % 100
    else:
        dial = (dial + num) % 100
    # Is it zero?
    if dial == 0: zeroes += 1

print('Part 1:', zeroes)

# Part 2 - Read the input again

# Reset the variables
dial = 50
zeroes = 0

for line in lines:
    # How far does the dial move?
    num = int(line[1:])
    # Which direction?
    if line.startswith('L'):
        # Count each time the dial clicks past zero
        for i in range(num):
            dial = (dial - 1) % 100
            # Is it zero?
           if dial == 0: zeroes += 1
    else:
        # Count each time the dial clicks past zero
        for i in range(num):
            dial = (dial + 1) % 100
            # Is it zero?
            if dial == 0: zeroes += 1

print('Part 2:', zeroes)
