import re
from collections import deque
import scipy

# Read the input
lines = open("10.in").read().splitlines()

toggle = {'.':'#', '#':'.'}

class Machine:
    def __init__(self, lights, wiring, joltages):
        self.lights = lights
        self.wiring = wiring
        self.joltages = joltages

    def part1(self):
        'Use a BFS to solve the indicator problem'
        q = deque()
        q.append((0, ['.' for x in self.lights] ))
        seen = set()
        while q:
            pushes, state = q.popleft()
            # Are we there yet?
            if self.lights == state:
                return pushes
            # Try to press each combination of buttons
            for wiring in self.wiring:
                # New result state
                nstate = []
                # Change the state of each indicator lights
                for i,light in enumerate(state):
                    if i in wiring:
                        nstate.append(toggle[state[i]])
                    else:
                        nstate.append(state[i])
                # Check if we've seen this state before
                if tuple(nstate) not in seen:
                    seen.add(tuple(nstate))
                    q.append((pushes+1, nstate))
        print('Found none')

    def part2(self):
        'Use SciPy to solve a matrix. 2D matrix of wiring x joltages.'
        # Start at joltages of 0
        A = [[0 for _ in range(len(self.wiring))] for j in range(len(self.joltages))]
        # Solve the entries which have non-zero effects when you press the buttons
        for j, button in enumerate(self.wiring):
            for light in button:
                A[light][j] = 1

        c = [1 for _ in range(len(self.wiring))]
        res = scipy.optimize.linprog(c, A_eq=A, b_eq=self.joltages, integrality=1)

        if not res.success:
            print("Couldn't find an optimal solution")
            return -1

        return sum(res.x)

machines = []

# Read in the source file and make each machine
for line in lines:
    lights = re.findall(r'[.#]', line)
    wiring_list = re.findall(r'(\(\S+\))', line)
    wiring = []
    for w in wiring_list:
        nw = [int(x) for x in w[1:-1].split(',')]
        wiring.append(nw)
    match = re.match('.*{(.+)}', line)
    joltages = [int(x) for x in match.groups(1)[0].split(',')]
    machine = Machine(lights, wiring, joltages)
    machines.append(machine)

print('Part 1:', sum([m.part1() for m in machines]))
print('Part 2:', sum([m.part2() for m in machines]))
