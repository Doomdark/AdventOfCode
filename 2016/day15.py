class Disc:
    def __init__(self, num, posns, start):
        self.num = num
        self.posns = posns
        self.posn = start
        self.initial = (num, posns, start)
    def next_posn(self):
        return (self.posn + 1) % self.posns
    def rotate(self):
        self.posn = self.next_posn()
        #print(self.num, self.posn)
    def set_time_zero(self):
        pass
    def reset(self):
        self.num, self.posns, self.posn = self.initial

discs = []

with open("day15_input.txt") as f:
    for line in f.readlines():
        l = line.strip().split()
        num = int(l[1][1:])
        posns = int(l[3])
        start = int(l[11].split('.')[0])
        disc = Disc(num, posns, start)
        discs.append(disc)

start_time = 0
while True:
    for disc in discs:
        disc.reset()
    #print(start_time)
    # Rotate the discs start_time times before starting
    for i in range(start_time):
        for disc in discs:
            disc.rotate()
    # Now rotate len(discs) times and see if thecapsulre makes it to the last disc
    for i in range(len(discs)):
        # Rotate all the discs
        for disc in discs:
            disc.rotate()
        # Is the current disc in posn 0?
        disc = None
        if discs[i].posn == 0:
            disc = discs[i]
        else: # Nope. Thie iteration doesn't work
            #print("disc in posn", discs[i].posn)
            break
    # If the loop finishes on the last disc then we got to the end
    if disc == discs[-1]:
        print("Part 1:", start_time)
        break

    start_time += 1
