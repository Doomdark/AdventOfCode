# Read the input
lines = open("11b.in").read().splitlines()

devices = {}

for line in lines:
    IN, OUTS = line.split(':')
    OUTS_ = OUTS.split()
    devices[IN] = OUTS_

DP = {}
trails = set()

def dfs(device, trail):
    # Already seen this combination?
    if device in DP:
        return DP[device]
    paths = 0
    ntrail = trail + [device]
    trails = 0
    moves = devices[device]
    for move in moves:
        if move == 'out':
            paths += 1
            print(ntrail + ['out'])
            if 'dac' in ntrail and 'fft' in ntrail:
                trails += 1
        else:
            _paths, _trails = dfs(move, ntrail)
            paths  += _paths
            if _trails >= 1:
                trails *= _trails
    DP[device] = (paths, trails)
    return (paths, trails)

p, t = dfs('svr', [])

print('Part 1:', p)
print('Part 2:', t)
