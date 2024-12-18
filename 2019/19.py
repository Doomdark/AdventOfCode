from collections import defaultdict

line = open('19.in').read()

program = defaultdict(lambda:0)
for n,c in enumerate(line.split(',')):
    program[n] = int(c)

X,Y = 10,10

from intcode import Intcode

pulled = set()
i=0
for y in range(Y):
    for x in range(X):
        i += 1
        d = Intcode(program)
        d.run()
        d.put(x)
        d.put(y)
        o = d.get()
        if o == 1:
            pulled.add((x,y))
        d.kill = True
        print(i, o, len(pulled))

print(len(pulled))
