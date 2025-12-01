from collections import defaultdict
import time

line = open('19.in').read()

program = defaultdict(int)
program.update({i:int(x.lstrip().rstrip()) for i,x in enumerate(line.split(','))})

X,Y = 2,2

from intcode import Intcode

pulled = set()
i=0
jobs = []

# Make a list of parallel jobs to run
# for y in range(Y):
#     for x in range(X):
#         d = Intcode(program)
#         d.put(x)
#         d.put(y)
#         d.x = x
#         d.y = y
#         jobs.append(d)

d = Intcode(program)
d.put(1)
d.put(1)
d.run()
print(d.get())
exit(0)

for job in jobs:
    # Start the thread, then start intcode
    job.start()
    job.run()

# Wait until all the jobs have finished
for job in jobs:
    job.join()

for job in jobs:
    o = job.get()
    if o == 1:
        pulled.add((job.x,job.y))
    print(job.x, job.y, o)

print(len(pulled))
