lines = open('25.in').read().splitlines()

locks   = []
keys    = []
row     = 0
item    = [None] * 5
is_lock = False

for line in lines:
    if not line:
        row = 0
        is_lock = False
    else:
        if row == 0 and line[0] == '#':
            is_lock = True
        for col,char in enumerate(line):
            if item[col] is None:
                if is_lock:
                    if char == '.': item[col] = row-1
                else:
                    if char == '#': item[col] = row
            if (row,col) == (6,4):
                if is_lock: locks.append(item)
                else:       keys.append(item)
                item = [None] * 5
        row += 1

fits = set()

for lock in locks:
    for key in keys:
        if all([k>l for k,l in zip(key,lock)]):
            fits.add(tuple(str(key)+str(lock)))

print('Part 1:', len(fits))
