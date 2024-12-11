STONES = '773 79858 0 71 213357 2937 1 3998391'

stones = STONES.split()

def apply(stones):
    _stones = []
    for stone in stones:
        istone = int(stone)
        if istone == 0:
            _stones.append('1')
        elif len(stone)%2 == 0:
            half = len(stone)>>1
            _stones.extend([str(int(stone[:half])), str(int(stone[half:]))])
        else:
            _stones.append(str(istone*2024))
    return _stones

for i in range(25):
    stones = apply(stones)

print('Part 1:', len(stones))

stones = STONES.split()
stones_orig = STONES.split()

increase = []
increase.append(len(stones))
inc_rate = []
SEEN = {}

for i in range(75):
    #SEEN[tuple(stones)] = i
    stones = apply(stones)
    matched = []
    for j,stone in enumerate(stones):
        for os in stones_orig:
            if len(matched) == 0: next_one = True
            elif j == matched[-1]+1: next_one = True
            else: next_one = False
            if os in stone and next_one:
                matched.append(j)
            else:
                matched = []
    if len(matched) == len(stones_orig):
        print(matched)
        exit
    # Is the list of stones repeated in the current list?
    # for k,v in SEEN.items():
    #     lstones = list(k)
    #     if lstones in stones:
    #         print('Repeat at', i)
    increase.append(len(stones))
    inc = increase[-1] - increase[-2]
    inc_rate.append(inc)
    if len(inc_rate) > 1:
        ir = inc_rate[-1] / inc_rate[-2]
    else:
        ir = inc_rate[0]
    print(i, len(stones), inc, ir)

print('Part 2:', len(stones))
