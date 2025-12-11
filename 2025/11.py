# Read the input
lines = open("11.in").read().splitlines()

devices = {}

for line in lines:
    IN, OUTS = line.split(':')
    OUTS_ = OUTS.split()
    devices[IN] = OUTS_

# out doesn't have a node
devices['out'] = []

def num_paths(start, end):
    # Cache the paths
    DP = {}

    def dfs(device):
        # Already seen this combination?
        if device in DP: return DP[device]
        # Initialise paths
        paths = 0
        # Go to all the output devices
        for move in devices[device]:
            # Are we at the end?
            if move == end: paths += 1
            # Nope, more iteration needed
            else: paths += dfs(move)
        # Say we've been here
        DP[device] = paths
        return paths

    return dfs(start)

print('Part 1:', num_paths('you', 'out'))

# Multiply up all the paths from svr->fft->dac->out and svr-dac->fft->out as
# doing all the paths is too much in one go.
svr_to_dac = num_paths('svr', 'dac')
dac_to_fft = num_paths('dac', 'fft')
fft_to_out = num_paths('fft', 'out')
svr_to_fft = num_paths('svr', 'fft')
fft_to_dac = num_paths('fft', 'dac')
dac_to_out = num_paths('dac', 'out')

print('Part 2:', (svr_to_dac*dac_to_fft*fft_to_out) + (svr_to_fft*fft_to_dac*dac_to_out))
