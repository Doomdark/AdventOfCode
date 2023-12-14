import copy

lines = open('14.in').read().splitlines()

rounds = set()
cubes  = set()

max_r, max_c = 0,0

# Load the grid into the sets
for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if char == '#':
            cubes.add((r,c))
        elif char == 'O':
            rounds.add((r,c))
        max_c = max(c, max_c)
    max_r = max(r,max_r)

# Save the initial state
original_rounds = copy.deepcopy(rounds)

def print_grid(count, rounds):
    'Print the grid for debug'
    print('-'*20, count)
    for r in range(max_r+1):
        row = ''
        for c in range(max_c+1):
            if (r,c) in cubes: row += '#'
            elif (r,c) in rounds: row += 'O'
            else: row += '.'
        print(row)

def move_north(rounds):
    global cubes
    # All columns
    for col in range(max_c+1):
        # All occupied column rows
        _col = [(r,c) for r,c in rounds|cubes if c == col]
        # Process each row starting at the top, sorted by incrementing row number
        for row in [r for r,c in sorted(_col, key=lambda a: a[0]) if (r,c) not in cubes]:
            # Max occupied square below this row
            max_row = max([r for (r,c) in _col if r < row], default = -1) + 1
            if max_row < row:
                rounds.remove((row,col))
                rounds.add((max_row,col))
                # Recalculate _col after changing rounds
                _col = [(r,c) for r,c in rounds|cubes if c == col]
    return rounds

def move_south(rounds):
    global cubes
    # All columns
    for i,col in enumerate(range(max_c+1)):
        # All occupied column rows
        _col = [(r,c) for r,c in rounds|cubes if c == col]
        # Process each row starting at the top, sorted by incrementing row number
        for row in [r for r,c in sorted(_col, key=lambda a: a[0], reverse=True) if (r,c) not in cubes]:
            # Max occupied square below this row
            min_row = min([r for (r,c) in _col if r > row], default = max_r+1) - 1
            if min_row > row:
                rounds.remove((row,col))
                rounds.add((min_row,col))
                # Recalculate _col after changing rounds
                _col = [(r,c) for r,c in rounds|cubes if c == col]
    return rounds

def move_west(rounds):
    global cubes
    # All rows
    for i,row in enumerate(range(max_r+1)):
        # All occupied row columnss
        _row = [(r,c) for r,c in rounds|cubes if r == row]
        # Process each row starting at the top, sorted by incrementing row number
        for col in [c for r,c in sorted(_row, key=lambda a: a[1]) if (r,c) not in cubes]:
            # Max occupied square below this row
            max_col = max([c for (r,c) in _row if c < col], default = -1) + 1
            if max_col < col:
                rounds.remove((row,col))
                rounds.add((row,max_col))
                # Recalculate _col after changing rounds
                _row = [(r,c) for r,c in rounds|cubes if r == row]
    return rounds

def move_east(rounds):
    global cubes
    # All rows
    for i,row in enumerate(range(max_r+1)):
        # All occupied row columnss
        _row = [(r,c) for r,c in rounds|cubes if r == row]
        # Process each row starting at the top, sorted by incrementing row number
        for col in [c for r,c in sorted(_row, key=lambda a: a[1], reverse=True) if (r,c) not in cubes]:
            # Max occupied square below this row
            min_col = min([c for (r,c) in _row if c > col], default = max_c+1) - 1
            if min_col > col:
                rounds.remove((row,col))
                rounds.add((row,min_col))
                # Recalculate _col after changing rounds
                _row = [(r,c) for r,c in rounds|cubes if r == row]
    return rounds

def load(rounds):
    total = 0
    for row in range(max_r+1):
        count = sum([1 for r,c in rounds if r == row])
        total += count * (max_r+1-row)
    return total

def part1(rounds):
    nrounds = move_north(rounds)
    return load(nrounds)

print('Part 1:', part1(rounds))

# Part 2:

state = {}
rounds = copy.deepcopy(original_rounds)

def cycle(rounds):
    nrounds = move_north(rounds)
    nrounds = move_west(nrounds)
    nrounds = move_south(nrounds)
    nrounds = move_east(nrounds)
    return nrounds

def part2(rounds):
    global state

    count = 0
    repeat = 0
    newstate = 0

    # Do cycles until there's a repeat
    while True:
        count += 1
        # Do a cycle
        rounds = cycle(rounds)
        # Make a unique state ID
        newstate = str(sorted(rounds))
        # is the state in the store already?
        if newstate in state:
            # Calculate the repeat length
            repeat = count - state[newstate][0]
            print('Cycles repeat at', count, 'with a repeat count of', repeat)
            break
        else: # Nope, add it, along with the current state
            state[newstate] = (count, copy.copy(rounds))

    # How many cycles left?
    left = (1000000000 - count) % repeat

    print('There are', left, 'cycles remaining')

    # Last state will be count - repeat + left
    match = count - repeat + left
    # Find that state in the dictionary
    for _, (_count, _rounds) in state.items():
        if _count == match:
            return load(_rounds)

    # Calculate the load
    return load(rounds)

print('Part 2:', part2(rounds))
