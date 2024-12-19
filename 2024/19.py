import heapq
from collections import defaultdict

lines = open('19.in').read().splitlines()

patterns = set(lines[0].split(', '))
towels = [x for x in lines[1:] if x]

def is_possible(towel):
    Q = []
    heapq.heappush(Q, 0)

    while Q:
        O = heapq._heappop_max(Q)
        # Test each pattern which can still fit in the string
        PATTERNS = [x for x in patterns if len(x) <= len(towel[O:]) and x]
        for P in sorted(PATTERNS, key=lambda s: len(s)):
            if towel[O:].startswith(P):
                # If the pattern length matches the remaining towel then it's a complete match
                if len(P) == len(towel[O:]):
                    return True
                elif len(P) < len(towel[O:]):
                    heapq.heappush(Q, O+len(P))

    return False

possible = 0
for towel in towels:
    possible += is_possible(towel)

print('Part 1:', possible)

# -- Part 2 --

# Got to count a gazillion possibilities in a tree so use a cache. Took me forever to realise this. :(
# The logic in the part 1 still works, you just have to add up everything.

from functools import cache

@cache
def dfs(towel, O=0):
    ways = 0
    PATTERNS = [x for x in patterns if len(x) <= len(towel[O:]) and x]
    for P in sorted(PATTERNS, key=lambda s: len(s)):
        if towel[O:].startswith(P):
            # If the pattern length matches the remaining towel then it's a complete match
            if len(P) == len(towel[O:]):
                ways += 1
            elif O+len(P) <= len(towel):
                ways += dfs(towel, O+len(P))
    return ways

ways = 0
for towel in towels:
    ways += dfs(towel)
print('Part 2:', ways)
