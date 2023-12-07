from collections import defaultdict

class Bot:
    def __init__(self):
        self.chips = set()
        self.high  = None
        self.low   = None
    def add_chip(self, chip):
        self.chips.add(chip)
    def has_two(self):
        return len(self.chips) == 2
    def delete_chip(self, chip):
        self.chips.remove(chip)
    def get_high(self):
        return max(self.chips)
    def get_low(self):
        return min(self.chips)
    def check(self, a,b):
        if a in self.chips and b in self.chips:
            return True

bots    = defaultdict(Bot)
outputs = {}

with open('day10.txt') as f:
    for line in f.readlines():
        _l = line.split()
        if _l[0] == 'value':
            value = int(_l[1])
            bot   = int(_l[5])
            if bot not in bots:
                bots[bot] = Bot()
            bots[bot].add_chip(value)
            #print(value, "goes to", bot)
        else:
            bot = int(_l[1])
            low = int(_l[6])
            low_dest = _l[5]
            high = int(_l[11])
            high_dest = _l[10]
            #print(bot,high_dest,high,low_dest,low)
            bots[bot].high = (high_dest,high)
            bots[bot].low  = (low_dest,low)
            #print(high_dest, low_dest)

finished = False
comparer = None

while not finished:
    bots_with_2 = 0

    for n,b in bots.items():

        # Check items for matching chips numbers for part 1
        if b.check(61,17):
            comparer = n

        # Has the bot got two chips?
        if b.has_two():
            bots_with_2 += 1

            dest, num = b.high
            h = b.get_high()
            #print(dest)
            if dest == 'output':
                if num not in outputs:
                    outputs[num] = []
                #print(h, num)
                outputs[num].append(h)
            else:
                #print("bot", num, "
                bots[num].add_chip(h)
            b.delete_chip(h)

            dest, num = b.low
            l = b.get_low()
            if dest == 'output':
                if num not in outputs:
                    outputs[num] = []
                #print(l, num)
                outputs[num].append(l)
            else:
                bots[num].add_chip(l)
            b.delete_chip(l)

    # Only exit when none of the bots has 2 chips
    if bots_with_2 == 0:
        finished = True

print("Part 1:", comparer)

print("Part 2:", outputs[0][0]*outputs[1][0]*outputs[2][0])
