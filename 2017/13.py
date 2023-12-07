layers = {}
max_layer = 0
max_depth = 0

with open('13.in') as f:
    for line in f.readlines():
        l,d = line.split(': ')
        layers[int(l)] = (int(d),0,1)
        max_layer = max(max_layer, int(l))
        max_depth = max(max_depth, int(d))

import copy
layers_copy = copy.deepcopy(layers)

def move_scanners():
    # Now move the scanners
    for layer, item in layers.items():
        d,l,_dir = item
        if _dir == 1:
            # Bottom of the layer
            if l == d-1:
                # Reverse
                _dir = -1
        elif _dir == -1:
            if l == 0:
                _dir = 1
        l += _dir
        item = (d,l,_dir)
        layers[layer] = item
    
def part1():
    global layers, max_layer
    severity = 0
    for i in range(max_layer+1):
        # Check if the scanner is here when we arrive
        if i in layers.keys():
            depth, level, _dir = layers[i]
            if level == 0:
                severity += i*depth
        move_scanners()

    return severity

def part2():
    global layers, max_layer
    for i in range(max_layer+1):
        # Check if the scanner is here when we arrive
        if i in layers.keys():
            depth, level, _dir = layers[i]
            if level == 0:
                return False
                #print('Caught on layer',i)
        #print_scanners(i)
        move_scanners()
        #print_scanners(i)

    return True

print('Part 1:', part1())
picoseconds = 0

def print_scanners(posn):
    s = ''
    for l in range(max_layer+1):
        s += ' {}  '.format(l)
    print(s)
    for d in range(max_depth+1):
        s = ''
        for l in range(max_layer+1):
            if l in layers.keys():
                _d,_l,_dir = layers[l]
                __d = 'S' if _dir == 1 else 's'
                if d<_d:
                    if d == 0 and l == posn:
                        s += '({}) '.format(__d if _l == d else ' ')
                    else:
                        s += '[{}] '.format(__d if _l == d else ' ')
                else:
                    s += '    '
            elif d == 0:
                if l == posn:
                    s += '(.) '
                else:
                    s += '... '
            else:
                s += '    '
        print(s)

# Try delays until not caught
done = False
loop = 3875838
while not done:
    print(loop)
    # Restore the starting position
    layers = copy.deepcopy(layers_copy)
    for j in range(loop):
        move_scanners()
    #print_scanners(0)
    done = part2()
    if done:
        print('Part 2:', loop)
    loop += 1
