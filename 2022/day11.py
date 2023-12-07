import copy
from math import lcm

class Monkey:
    def __init__(self, num, items, operation, test, true, false):
        self.num = num
        self.items = items
        self.operation = operation
        self.test = test
        self.true = true
        self.false = false
        self.inspected = 0

    def do_test(self, div3=True):
        # Test each item
        items = copy.copy(self.items)
        for item in items:
            #print('{} checking {}'.format( self.num, item))
            # Update worry level
            worry = 0
            if self.operation[1] == 'old':
                val = item
            else:
                val = int(self.operation[1])
            if self.operation[0] == '*':
                worry = item * val
            elif self.operation[0] == '+':
                worry = item + val
            #print('Worry:',worry)
            # Gets bored
            if div3:
                worry = worry//3

            # Divide the worry by the greatest common divisor
            worry = worry % least_common_mult

            #print('Worry2:',worry)
            # Test
            test = (worry%self.test == 0)

            if test:
                #print('True:',self.true)
                monkeys[self.true].items.append(worry)
            else:
                #print('False',self.false)
                monkeys[self.false].items.append(worry)
            # Remove this item from the list
            self.items = self.items[1:]
            # Increment inspections
            self.inspected += 1

    def __str__(self):
        l = []
        l.append('Monkey {}:'.format(self.num))
        l.append('  Items:     {}'.format(self.items))
        l.append('  Operation: {}'.format(self.operation))
        l.append('  Test:      {}'.format(self.test))
        l.append('    False:   {}'.format(self.false))
        l.append('    True:    {}'.format(self.true))
        l.append('    I:       {}'.format(self.inspected))
        return '\n'.join(l)

lines = open("11.in").read().splitlines()

monkeys = []

num = 0
items = []
divisors = []
operation = None

for line in lines:
    if line.startswith('Monkey'):
        l = line.split()
        num = int(l[1][:-1])
        #print('Monkey:',num)
    elif line.startswith('  Starting items: '):
        l = line.split('  Starting items: ')
        items = [int(x) for x in l[-1].split(', ')]
        #print('Items:',items)
    elif 'Operation' in line:
        l = line.split('  Operation: ')[-1].split()[-2:]
        #print('Operation:',l)
        operation = l
    elif 'Test' in line:
        l = line.split()
        test = int(l[-1])
        #print('Test:',test)
        divisors.append(test)
    elif 'false' in line:
        l = line.split()
        false = int(l[-1])
        #print('False:',false_outcome)
    elif 'true' in line:
        l = line.split()
        true = int(l[-1])
        #print('True:',true_outcome)
    else:
        m = Monkey(num, items, operation, test, true, false)
        monkeys.append(m)

# Add the last one
m = Monkey(num, items, operation, test, true, false)
monkeys.append(m)

least_common_mult = lcm(*divisors)

# Do rounds
for i in range(20):
    for m in monkeys:
        m.do_test()

inspections = sorted([m.inspected for m in monkeys])
print('Part 1:', inspections[-1] * inspections[-2])

monkeys = []

num = 0
items = []
divisors = []
operation = None

for line in lines:
    if line.startswith('Monkey'):
        l = line.split()
        num = int(l[1][:-1])
        #print('Monkey:',num)
    elif line.startswith('  Starting items: '):
        l = line.split('  Starting items: ')
        items = [int(x) for x in l[-1].split(', ')]
        #print('Items:',items)
    elif 'Operation' in line:
        l = line.split('  Operation: ')[-1].split()[-2:]
        #print('Operation:',l)
        operation = l
    elif 'Test' in line:
        l = line.split()
        test = int(l[-1])
        divisors.append(test)
        #print('Test:',test)
    elif 'false' in line:
        l = line.split()
        false = int(l[-1])
        #print('False:',false_outcome)
    elif 'true' in line:
        l = line.split()
        true = int(l[-1])
        #print('True:',true_outcome)
    else:
        m = Monkey(num, items, operation, test, true, false)
        monkeys.append(m)

# Add the last one
m = Monkey(num, items, operation, test, true, false)
monkeys.append(m)

gcdivisor = lcm(*divisors)

## Part 2 ##
for i in range(10000):
    for m in monkeys:
        m.do_test(False)

inspections = sorted([m.inspected for m in monkeys])
print('Part 2:', inspections[-1] * inspections[-2])
