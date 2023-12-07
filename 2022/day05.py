stacks = {}
moves = []

with open("day05_input.txt") as f:
    for line in f.readlines():
        # Iterate each character in the line
        if line.startswith('move'):
            l = line.strip().split()
            quantity,src,dst = int(l[1]), int(l[3])-1, int(l[5])-1
            moves.append((quantity,src,dst))
        # Ignore the line with the crate numbers on it
        elif line.startswith(" 1"):
            pass
        # Ignore any empty lines
        elif line == '\n':
            pass
        else: # Parse the crates
            # Do the crates by character
            for c,char in enumerate(line):
                # A crate will be at position 1,5,9,etc.
                if (c-1) % 4 == 0:
                    # Check if we've got A-Z
                    if ord(char) in range(65,91):
                        # The stack number goes in 4's
                        stack_num = (c-1) // 4
                        # Add a new stack if there isnt one
                        if stack_num not in stacks:
                            stacks[stack_num] = []
                        # Add the crate to the stack
                        stacks[stack_num].append(char)

# Reverse the order of all the stacks now they've been read in
for stack in stacks.keys():
    stacks[stack] = list(reversed(stacks[stack]))

# Keep a copy of the original stacks for part 2
import copy
stacks_copy = copy.deepcopy(stacks)

## Part 1 ##

# Do the part 1 moves
for move in moves:
    quantity,s,d = move
    # Move a crate at a time
    for i in range(quantity):
        stacks[d].append(stacks[s].pop())

ends = [v[-1] for k,v in sorted(stacks.items())]
print('Part 1:', ''.join(ends))

## Part 2 ##

# Use the saved stacks
stacks = stacks_copy

# Do the part 2 moves
for move in moves:
    quantity,s,d = move
    # Move multiple crate at a time in the same order
    stacks[d].extend(stacks[s][-quantity:])
    # Dump the end of the source stack
    stacks[s] = stacks[s][:-quantity]

ends = [v[-1] for k,v in sorted(stacks.items())]
print('Part 2:', ''.join(ends))
