import itertools
import re
from collections import defaultdict

lines = open('05.in').read().splitlines()

seeds = []

src_name = ''
dst_name = ''

map_moves = {}
ranges = defaultdict(list)

for line in lines:
    if line.startswith('seeds:'):
        seeds = [int(x) for x in re.findall('\d+', line)]
    elif line.endswith('map:'):
        n,m = line.split()
        src_name,t,dst_name = n.split('-')
        map_moves[src_name] = dst_name
    elif len(line) > 0:
        dst, src, rng = re.findall('\d+', line)
        ranges[src_name].append((int(src), int(dst), int(rng)))

def recurse(thing):
    # Location is the final value
    if thing[1] == 'location':
        return thing[0]
    # Iterate through all the ranges given by thing[1]
    for src, dst, rng in ranges[thing[1]]:
        # Is the provided number in range?
        if src <= thing[0] < src+rng:
            newthing = (thing[0]-src+dst, map_moves[thing[1]])
            return recurse(newthing)
    # Seed doesn't exist - use the provided value
    newthing = (thing[0], map_moves[thing[1]])
    return recurse(newthing)

lowest = 999999999999999999

for seed in seeds:
    loc = recurse((seed, 'seed'))
    lowest = min(loc, lowest)

print('Part 1:', lowest)

# Part 2

new_seeds = []

lowest = 999999999999999999

def get_val_from_map(map_name, value):
    for entry in ranges[map_name]:
        src, dst, rng = entry
        if dst <= value < dst+rng:
            return src + (value - dst)
    return value

def part2():
    # Just try all locations starting from 0 as we're looking for the lowest location
    for val in itertools.count():
        # Get the values from the maps in reverse
        humidity    = get_val_from_map('humidity',    val)
        temperature = get_val_from_map('temperature', humidity)
        light       = get_val_from_map('light',       temperature)
        water       = get_val_from_map('water',       light)
        fertilizer  = get_val_from_map('fertilizer',  water)
        soil        = get_val_from_map('soil',        fertilizer)
        seed        = get_val_from_map('seed',        soil)
        # Is the seed location within any seed ranges?
        for src, rng in zip(seeds[::2], seeds[1::2]):
            if src <= seed < src+rng:
                print('Part 2:', val)
                exit(0)

part2()

