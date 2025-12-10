import re, heapq
import multiprocessing as mp
from collections import deque

# Read the input
lines = open("10a.in").read().splitlines()

toggle = {'.':'#', '#':'.'}

class Machine:
    def __init__(self, lights, wiring, joltages):
        self.lights = lights
        self.wiring = wiring
        self.joltages = joltages
        self.pushes = 0

    def part1(self):
        #q = []
        q = deque()
        #heapq.heappush(q, (0, ['.' for x in self.lights] ))
        q.append((0, ['.' for x in self.lights] ))
        while q:
            #pushes, state = heapq.heappop(q)
            pushes, state = q.popleft()
            #print(pushes, len(q))
            if self.lights == state:
                self.pushes = pushes
                print(pushes)
                return pushes
            # Try to press each combination of buttons
            for wiring in self.wiring:
                # New resulting state
                nstate = []
                # Change the state of each indicator lights
                for i,light in enumerate(state):
                    if i in wiring:
                        nstate.append(toggle[state[i]])
                    else:
                        nstate.append(state[i])
                #heapq.heappush(q, (pushes+1, nstate))
                q.append((pushes+1, nstate))
        print('Found none')

    def part2(self):
        q = deque()
        q.append((0, [0 for x in self.joltages] ))
        print(q)
        while q:
            pushes, state = q.popleft()
            if self.joltages == state:
                return pushes
            # If any values in the state are bigger than the wanted joltages then continue
            for wiring in self.wiring:
                # New resulting state
                nstate = []
                # Change the state of each indicator lights
                for i,joltage in enumerate(state):
                    if i in wiring:
                        nstate.append(joltage+1)
                    else:
                        nstate.append(joltage)
                #heapq.heappush(q, (pushes+1, nstate))
                q.append((pushes+1, nstate))
                print(pushes+1,nstate)
        print('Found none')

machines = []

for line in lines:
    lights = re.findall(r'[.#]', line)
    wiring_list = re.findall(r'(\(\S+\))', line)
    wiring = []
    for w in wiring_list:
        nw = [int(x) for x in w[1:-1].split(',')]
        wiring.append(nw)
    match = re.match('.*{(\S+)}', line)
    joltages = [int(x) for x in match.groups(1)[0].split(',')]
    machine = Machine(lights, wiring, joltages)
    machines.append(machine)
    print(lights, wiring, joltages)

# jobs = []
# for m in machines:
#     job = mp.Process(target=m.part1)
#     jobs.append(job)
#
# for job in jobs:
#     job.start()
#
# for job in jobs:
#     job.join()
#
# print('Part 1:', sum([m.pushes for m in machines]) )
# exit(0)

#print(machines[0].pushes)
# total = 0
# i = 0
# for m in machines:
#     total += m.part1()
#     print(i, total)
#     i += 1

#print('Part 1:', sum([m.part1() for m in machines]))
print('Part 2:', sum([m.part2() for m in machines]))
