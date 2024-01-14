from collections import deque
import copy

programs = deque()
for i in 'abcdefghijklmnop':
    programs.append(i)

moves = open('16.in').read().split(',')

def dance():
    for move in moves:
        inst = move[0]
        # Spin
        if inst == 's':
            val = int(move[1:])
            programs.rotate(val)
        # Not spin
        else:
            a,b = 0,0
            # Exchange
            if inst == 'x':
                a,b = [int(x) for x in move[1:].split('/')]
            # Partner
            elif inst == 'p':
                _a,_b = [x for x in move[1:].split('/')]
                a = programs.index(_a)
                b = programs.index(_b)
            # Do the move
            temp = copy.deepcopy(programs[a])
            programs[a] = programs[b]
            programs[b] = temp

dance()

print('Part 1:', ''.join(programs))

# Part 2 needs the state preserved

def part2():
    states = {}
    # Keep the state from part 1
    ID = ''.join(programs)
    states[ID] = 1
    count = 1
    # Run until we find a matching state
    while True:
        count += 1
        dance()
        ID = ''.join(programs)
        # Add the new state
        if ID not in states:
            states[ID] = count
        else:
            # State seen before so determine the repeat
            repeat = count - states[ID]
            # Number of cycles left after repeats have been applied
            left = (1000000000 - count) % repeat
            # The count of the final state after all the cycles have happened
            match = count - repeat + left
            # Get the value of the state for this count
            for state, count in states.items():
                if match == count:
                    return state

print('Part 2:', part2())
