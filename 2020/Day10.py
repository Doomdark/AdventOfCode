adapters = []

with open("Day10_input.txt") as f:
    for line in f.readlines():
        adapters.append(int(line.rstrip()))

adapters.sort()
adapters = [0] + adapters + [adapters[-1]+3]

diffs = {}
diffs[0] = 0
diffs[1] = 0
diffs[2] = 0
diffs[3] = 0

def part1():
    last = 0
    for a in adapters:
        diff = a - last
        diffs[diff] += 1
        last = a
    print (diffs[1] * diffs[3], diffs)

part1()

def part2():
    dp = [1]
    for i in range(1, len(adapters)):
        ans = 0
        for j in range(i):
            if adapters[j] + 3 >= adapters[i]:
                ans += dp[j]
        dp.append(ans)
    print (dp[-1])

part2()
