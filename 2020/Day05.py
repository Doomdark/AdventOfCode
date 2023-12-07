highest = 0
populated = {}

for i in range(874):
    populated[i] = 0

with open("Day05_input.txt") as f:
    for line in f.readlines():
        id = int((line.rstrip()).replace('F','0').replace('B','1').replace('L','0').replace('R','1'),2)
        populated[id] = 1
        if id > highest:
            highest = id

print ("Part 1:", highest)

val = 0
for k,v in populated.items():
    if v == 0:
        val = k
        
print ("Part 2:",val)
        
