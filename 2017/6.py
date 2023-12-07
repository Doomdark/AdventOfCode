seen = set()

banks = [0,2,7,0]
banks = []

with open("6.in") as f:
    for line in f.readlines():
        banks.extend([int(x) for x in line.strip().split()])

seen.add(tuple(banks))

cycles = 0
part2_check = None

while True:
    bmax = max(banks)
    bmaxindex = banks.index(bmax)
    redist = int(banks[bmaxindex])
    banks[bmaxindex] = 0
    for i in range(redist):
        banks[(i+bmaxindex+1)%len(banks)] += 1

    #print(cycles, bmax, bmaxindex, banks)

    cycles += 1

    #if cycles == 10: sys.exit()

    if tuple(banks) in seen:
        print("Part 1:", cycles)
        part2_check = tuple(banks)
        break

    seen.add(tuple(banks))

cycles = 0

while True:
    bmax = max(banks)
    bmaxindex = banks.index(bmax)
    redist = int(banks[bmaxindex])
    banks[bmaxindex] = 0
    for i in range(redist):
        banks[(i+bmaxindex+1)%len(banks)] += 1

    #print(cycles, bmax, bmaxindex, banks)

    cycles += 1

    #if cycles == 10: sys.exit()

    if tuple(banks) == part2_check:
        print("Part 2:", cycles)
        break
