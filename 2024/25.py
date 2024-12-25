lines = open('25.in').read().splitlines()

keys  = []
locks = []

row = 0
item = set()

for line in lines:
    if not line:
        row = 0
        item = set()
    else:
        for col,char in enumerate(line):
            if char == '#': item.add((row,col))
            if (row,col) == (6,4):
                if (0,0) in item: locks.append(item)
                else:             keys.append(item)
        row += 1

FITS = set()

for lock in locks:
    lock_heights = []
    for lcol in range(5):
        lock_heights.append(max([r for r,c in lock if c == lcol]))
    
    for key in keys:
        key_heights = []
        for kcol in range(5):
            key_heights.append(min([r for r,c in key if c == kcol]))

        fits = True
        for n in range(len(key_heights)):
            if key_heights[n] <= lock_heights[n]:
                fits = False
                
        if fits:
            FITS.add(tuple(str(key_heights)+str(lock_heights)))
            
print('Part 1:', len(FITS))
