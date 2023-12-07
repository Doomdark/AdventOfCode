import copy
elves = []

count = 3004953
#count = 5

class Elf:
    def __init__(self, num):
        self.num = num
        self.presents = 1
        self.next = None

    def add(self, presents):
        #print('Adding {} presents to elf {}'.format(presents, self.num))
        self.presents += presents

    def __repr__(self):
        return 'Elf {} has {} presents. Next elf is {}'.format(self.num, self.presents, self.next.num)
        
# Make the elves and link them up
for i in range(count):
    elves.append(Elf(i))
for i in range(count-1):
    elves[i].next = elves[i+1]
elves[count-1].next = elves[0]

# Starting Elf
elf = elves[0]

while True:
    #print(elf)
    elf.add(elf.next.presents)
    elf.next = elf.next.next
    if elf.next == elf:
        print('Part 1:', elf.num+1)
        break
    next_elf = elf.next
    elf = next_elf

# Part 2
elves = []
for i in range(count):
    elves.append(Elf(i))
    
posn = 0
while len(elves) > 1:
    lelves = len(elves)
    #print(posn, len(elves))
    # Copy the current list
    new_elves = elves.copy()
    cur_elf  = elves[posn]
    next_elf = elves[(posn+(lelves//2))%lelves]
    # Update the current elf
    #print("Elf", cur_elf[0]+1, 'takes elf', next_elf[0]+1,"'s", next_elf[1], 'presents')
    cur_elf.add(next_elf.presents)
    new_elves[posn] = cur_elf
    # Get the index of the elf we're about to remove
    rindex = new_elves.index(next_elf)
    new_elves = new_elves[:rindex] + new_elves[rindex+1:]
    elves = new_elves
    if posn >= len(elves):
        posn = 0
    else:
        posn = posn+1 %len(elves)

print('Part 2:', elves[0].num+1)
