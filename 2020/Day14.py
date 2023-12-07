mem = {}
andmask  = 0
ormask  = 0

import re
mask_filt = re.compile('mask = (\w+)')
mem_filt  = re.compile(r'mem\[(\d+)\] = (\d+)')

def make_mask(newmask):
    _and = 0
    _or  = 0
    for char in newmask:
        _and = _and << 1
        _or  = _or << 1
        if   char == 'X': _and += 1
        elif char == '1': _or  += 1
    return _and, _or

# Make a list of addresses that have X in them. Replace each X with 0 and 1 for each address.
# This is recursive. I hate recursive functions.
def get_addrs(addrs, addr):
    if addr.count('X') == 0:
        _a = 0
        for x in addr:
            _a = _a << 1
            _a += int(x)
        addrs.append(_a)
        return
    get_addrs(addrs, addr.replace('X','0',1))
    get_addrs(addrs, addr.replace('X','1',1))

with open("Day14_input.txt") as f:
    for line in f.readlines():
        mask_match = mask_filt.match(line.rstrip())
        if mask_match:
            andmask, ormask = make_mask(mask_match.group(1))
        mem_match = mem_filt.match(line.rstrip())
        if mem_match:
            addr = int(mem_match.group(1))
            val  = int(mem_match.group(2))
            mem[addr] = (val & andmask) | ormask

    print ("Part 1:", sum([x for x in mem.values()]))
          
mem = {}
andmask = 0
ormask  = 0
addrs = []

def make_mask2(newmask):
    _and = 0
    _or  = 0
    for char in newmask:
        _and = _and << 1
        _or  = _or << 1
        # Overwrite bits set to 1
        if char == '1':
            _or  += 1
            # Mask out the floating bits
        elif char != "X":
            _and += 1
    return _and, _or

with open("Day14_input.txt") as f:
    for line in f.readlines():
        mask_match = mask_filt.match(line.rstrip())
        if mask_match:
            addrs = []
            mask = mask_match.group(1)
            # Make the and and or masks differently
            andmask, ormask = make_mask2(mask)
            # Get a list of floating addresses
            get_addrs(addrs, mask.replace('1','0'))
        mem_match = mem_filt.match(line.rstrip())
        if mem_match:
            addr = int(mem_match.group(1))
            val  = int(mem_match.group(2))
            # For each combination of addr and floating, update the memory address
            for f in addrs:
                _a = f+((addr&andmask)|ormask)
                mem[_a] = val

    print ("Part 2:", sum([x for x in mem.values()]))
