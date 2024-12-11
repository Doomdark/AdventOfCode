STONES = '773 79858 0 71 213357 2937 1 3998391'

stones = tuple(STONES.split())

def apply(stones):
    _stones = []
    for stone in stones:
        istone = int(stone)
        if istone == 0:
            _stones += ['1']
        elif len(stone)%2 == 0:
            half = len(stone)>>1
            _stones += [ str(int(stone[:half])), str(int(stone[half:])) ]
        else:
            _stones += [ str(istone*2024) ]
    return _stones

for i in range(25):
    stones = apply(stones)

print('Part 1:', len(stones))

stones = STONES.split()

nstones = []
# Do each stone individually
for j,stone in enumerate(stones):
    _stones = [stone]
    for i in range(75):
        _stones = apply(_stones)
        print(j,i, len(_stones))
    nstones.append(len(_stones))

print('Part 2:', sum(nstones))
