import itertools
import re
from collections import defaultdict

lines = open('05.in').read().splitlines()

seeds = []

src_name = ''
dst_name = ''

ranges = defaultdict(list)

for line in lines:
    if line.startswith('seeds:'):
        seeds = [int(x) for x in re.findall('\d+', line)]
    elif line.endswith('map:'):
        n,m = line.split()
        src_name,t,dst_name = n.split('-')
    elif len(line) > 0:
        dst, src, rng = [int(x) for x in re.findall('\d+', line)]
        ## # Check for overlapping destinations
        ## for d,s,r in ranges[src_name]:
        ##     dmax = d+r-1
        ##     if (d <= dst <= dmax) or (d <= dst+rng-1 <= dmax) or (dst < d and dmax < dst+rng-1):
        ##         print('Overlapping dst ranges: {} -> {} and {} -> {}'.format(d,dmax,dst,dst+rng-1 ))
        ranges[src_name].append([dst,src,rng])

# Part 1

def get_dst_from_map(map_name, value):
    for entry in ranges[map_name]:
        dst, src, rng = entry
        if src <= value < src+rng:
            return dst + (value - src)
    return value

def part1():
    lowest = 99999999999999999999
    # Iterate through the seeds
    for seed in seeds:
        # Get the values from the maps
        soil        = get_dst_from_map('seed',        seed)
        fertilizer  = get_dst_from_map('soil',        soil)
        water       = get_dst_from_map('fertilizer',  fertilizer)
        light       = get_dst_from_map('water',       water)
        temperature = get_dst_from_map('light',       light)
        humidity    = get_dst_from_map('temperature', temperature)
        location    = get_dst_from_map('humidity',    humidity)
        # Find the lowest location value
        lowest = min(location, lowest)

    return lowest

print('Part 1:', part1())

# Part 2

# Reverse the lookup, starting from location 0 and incrementing the location number until it
# matches a valid seed number in the original list.

def get_src_from_map(map_name, value):
    for entry in ranges[map_name]:
        dst, src, rng = entry
        if dst <= value < dst+rng:
            return src + (value - dst)
    return value

def part2():
    # Just try all locations starting from 0 as we're looking for the lowest location
    for location in itertools.count():
        # Get the values from the maps in reverse
        humidity    = get_src_from_map('humidity',    location)
        temperature = get_src_from_map('temperature', humidity)
        light       = get_src_from_map('light',       temperature)
        water       = get_src_from_map('water',       light)
        fertilizer  = get_src_from_map('fertilizer',  water)
        soil        = get_src_from_map('soil',        fertilizer)
        seed        = get_src_from_map('seed',        soil)
        # Is the seed location within any seed ranges?
        for src, rng in zip(seeds[::2], seeds[1::2]):
            # Is the seed number in one of the seed ranges?
            if src <= seed < src+rng:
                print('Part 2:', location)
                exit(0)

part2()
