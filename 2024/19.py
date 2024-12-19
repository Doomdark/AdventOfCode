lines = open('19.in').read().splitlines()

patterns = set(lines[0].split(', '))
towels = [x for x in lines[1:] if x]

DP = {}
POSSIBLES = 0
WAYS = 0

def dfs(towel, O=0):
    # Already seen this combination?
    if (towel,O) in DP:
        return DP[(towel,O)]
    ways = 0
    # Test against patterns which fit entirely into the remaining towel length
    PATTERNS = [x for x in patterns if len(x) <= len(towel[O:]) and x]
    for P in PATTERNS:
        if towel[O:].startswith(P):
            # If the pattern length matches the remaining towel then it's a complete match
            if len(P) == len(towel[O:]):
                ways += 1
            else:
                ways += dfs(towel, O+len(P))
    # Cache the result for later
    DP[(towel,O)] = ways
    return ways

for towel in towels:
    n = dfs(towel)
    POSSIBLES += (n > 0)
    WAYS += n

print('Part 1:', POSSIBLES)
print('Part 2:', WAYS)
