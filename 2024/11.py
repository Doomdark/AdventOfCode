stones = '773 79858 0 71 213357 2937 1 3998391'.split()

from collections import defaultdict

def apply(stone):
    _stones = []
    istone = int(stone)
    if istone == 0:
        _stones += ['1']
    elif len(stone)%2 == 0:
        half = len(stone)>>1
        _stones += [ str(int(stone[:half])), str(int(stone[half:])) ]
    else:
        _stones += [ str(istone*2024) ]
    return tuple(_stones)

def solve(loops=25):
    global stones
    S = {stone:1 for stone in stones}
    for i in range(loops):
        _S = defaultdict(int)
        for stone, count in S.items():
            _stones = apply(stone)
            for s in _stones:
                _S[s] += count
        S = _S
    return sum(S.values())

print('Part 1:', solve())
print('Part 2:', solve(75))
