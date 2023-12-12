lines = open('12.in').read().splitlines()

import re
from collections import defaultdict
from itertools import product
import functools

# Brute force method for part 1...

if False:

    total = 0

    # iterate through the lines
    for line in lines:
        pattern, _nums = line.split()
        nums = [int(x) for x in _nums.split(',')]
        print(pattern, nums)
        # No matches yet
        count = 0
        # No repeats
        done = set()
        # Make all possible combinations
        combs = product('.#', repeat=pattern.count('?'))
        # Iterate through the combinations
        for comb in combs:
            npattern = ''
            posn = 0
            for i,char in enumerate(pattern):
                if char == '?':
                    npattern += str(comb[posn])
                    posn += 1
                else:
                    npattern += char
            # Split the new pattern into chunks
            _npattern = [x.count('#') for x in npattern.replace('.',' ').split()]
            # Matching chunk count
            if len(_npattern) != len(nums): continue
            # Matching length count
            if _npattern != nums: continue
            # Match
            print('MATCH', npattern, nums)
            if npattern not in done:
                count += 1
                #done.add(npattern)
        # Add on the count to the total
        total += count

    print('Part 1:', total)
    exit(0)

# OK, that approach isn't going to work for part 2 because part 2 has a *much* bigger state space.
# What we need is a DFS to check each possibility in turn. And a cache.

@functools.lru_cache(None)
def recurse(string, nums, string_index, nums_index, count):
    # Have we got to the end of the string yet?
    if string_index == len(string):
        # Got to the end of the blocks and the current block count is 0 so it's a match
        if nums_index == len(nums) and count == 0:
            return 1
        # If we're on the last block and the current block count matches then the block finished at the end of the line
        elif nums_index == len(nums)-1 and count == nums[nums_index]:
            return 1
        # Otherwise we weren't successful
        else:
            return 0
    score = 0
    # Try the next bit in the pattern. It can be either . or #.
    for char in '.#':
        # What's the character in the current string? It can be either ? or the selected char.
        if string[string_index] == char or string[string_index] == '?':
            # Check for ' and if we're not inside a block yet
            if char == '.' and count == 0:
                # Move on to the next string entry using the same block index and a zero block count
                score += recurse(string, nums, string_index+1, nums_index, 0)
            # Got a . when we're inside a block, haven't run out of blocks, but have reached the end of the current block
            elif char == '.' and count > 0 and nums_index < len(nums) and nums[nums_index] == count:
                # Increment the string index and nums index and reset the block count
                score += recurse(string, nums, string_index+1, nums_index+1, 0)
            # Got a #
            elif char == '#':
                # Increment the string index and the block count
                score += recurse(string, nums, string_index+1, nums_index, count+1)
            # If it's none of these then we shouldn't take this path any further
    return score

for part2 in [False, True]:
    total = 0

    # Process all the patterns
    for line in lines:
        pattern, nums = line.split()

        # For part 2 multiply everything up by 5
        if part2:
            pattern = '?'.join([pattern]*5)
            nums    = ','.join([nums]*5)

        # Split the numbers up into a list
        nums = tuple([int(x) for x in nums.split(',')])

        # Need to count the string position, block index, and current length of block.
        total += recurse(pattern, nums, 0, 0, 0)

    if not part2:
        print('Part 1:', total)
    else:
        print('Part 2:', total)
