from collections import defaultdict

Sues = defaultdict(dict)

lines = open("16.in").read().splitlines()

for line in lines:
    # First 2 items are the Sue
    l = line.split()
    num = int(l[1].replace(':',''))
    ll = l[2:]
    for thing,count in zip(ll[::2],ll[1::2]):
        Sues[num][thing.replace(':','')] = int(count.replace(',',''))

def solve(part2=False):
    global Sues
    # Looking for:
    find = defaultdict(dict)
    find['children']    = 3
    find['cats']        = 7
    find['samoyeds']    = 2
    find['pomeranians'] = 3
    find['akitas']      = 0
    find['vizslas']     = 0
    find['goldfish']    = 5
    find['trees']       = 3
    find['cars']        = 2
    find['perfumes']    = 1

    for num,sue in Sues.items():
        found = True
        for item in ['children', 'cats', 'samoyeds', 'pomeranians', 'akitas',
                      'vizslas', 'goldfish', 'trees', 'cars', 'perfumes']:
            if item not in sue:
                continue
            if part2:
                if item in ['trees','cats']:
                    if sue[item] <= find[item]:
                        found = False
                        break
                elif item in ['pomeranians','goldfish']:
                    if sue[item] >= find[item]:
                        found = False
                        break
                else:
                    if sue[item] != find[item]:
                        found = False
                        break
            else:
                if sue[item] != find[item]:
                    found = False
                    break
        if found:
            return num

    return Sue
print('Part 1:', solve())
print('Part 2:', solve(True))
