from collections import deque, defaultdict
import re

ore_robots = 1
clay_robots = 0
obsidian_robots = 0
geode_robots = 0

ore = 0
clay = 0
obsidian = 0
geodes = 0

lines = open("19.ex").read().splitlines()

blueprints = []

for line in lines:
    numbers = re.findall('\d+', line)
    blueprints.append([int(x) for x in numbers])

# Max geode stores
max_geodes = defaultdict(int)

import multiprocessing as mp

Queue = mp.Queue

def dfs(T):
