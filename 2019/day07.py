import intcode, itertools, sys, threading

from intcode import Intcode

program = {i:int(x) for i,x in enumerate(open("day07_input.txt",'r').read().strip().split(','))}

#program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
#program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
#program = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
max = 0

class Amp(Intcode, threading.Thread):
    def __init__(self, program, phase, num):
        threading.Thread.__init__(self)
        Intcode.__init__(self, program)
        self.input_queue.put(phase)
        self.num = num
        self.phase = phase
        #print "Amp phase", phase

    def run(self):
        Intcode.run(self)

    def amplify(self, _input):
        self.input_queue.put(_input)
        while self.running:
            if self._exit:
                break
        _output = self.output_queue.get()
        return _output

phases = [0,1,2,3,4]

# Initialise the amps for each permutation
count = 0
for perm in itertools.permutations(phases, 5):
    amps = []
    # Create the amps
    for p in list(perm):
        a = Amp(program, p, count)
        amps.append(a)
        a.start()
        count += 1

    b = 0
    for a in amps:
        b = a.amplify(b)
    if b > max:
        max = b

print("Part 1: ", max)

# Part 2 has different phases
phases = [9,8,7,6,5]

# Initialise the amps for each permutation
count = 0
max = 0

# Test all initial phase permutations
for perm in itertools.permutations(phases, 5):
    amps = []
    # Create the amps
    for p in list(perm):
        a = Amp(program, p, count)
        amps.append(a)
        a.start()
        count += 1

    b = 0
    # Run until all the amps are finished
    while 1:
        for a in amps:
            b = a.amplify(b)
        if b > max:
            max = b
        if amps[0]._exit:
            break

print("Part 2: ", max)
