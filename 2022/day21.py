lines = open("21.in").read().splitlines()

monkeys = {}

inverse = {'/':'*', '*':'/', '+':'-', '-':'+'}

class Monkey:
    def __init__(self, name, expr):
        self.name = name
        self.kids = []
        self.expr = None
        try:
            self.expr = int(expr)
        except:
            l = expr.split()
            self.kids.extend([l[0], l[2]])
            self.math = l[1]

    def get_sum(self):
        result = 0
        if self.kids:
            vals = []
            for kid in self.kids:
                vals.append(monkeys[kid].get_sum())
            result = int(eval('{} {} {}'.format(vals[0], self.math, vals[1])))
            return result
        else:
            return self.expr

    def __repr__(self):
        if isinstance(self.expr, int):
            return self.expr
        else:
            return '{}{}{}'.format(self.kids[0], self.math, self.kids[1])

# Process the input
for line in lines:
    m, expr = line.split(': ')
    monkey = Monkey(m, expr)
    monkeys[m] = monkey

print("Part 1: {}".format(monkeys['root'].get_sum()))

## Part 2 ##

# Do a top-down invert of the expressions.
# The LHS of the root equality is static.
# Iterate down the RHS and whichever branch can be evaluated, perform the inverse operation on the LHS.
# Then go down the next branch.

# Remove humn from the monkeys list. Then the expression can't evaluate.
del monkeys['humn']

def invert(value, node):
    l  = monkeys[node].kids[0]
    r  = monkeys[node].kids[1]
    op = monkeys[node].math
    has_humn = None
    try:
        L = monkeys[l].get_sum()
    except KeyError:
        # This side has humn
        has_humn = 'L'
    try:
        R = monkeys[r].get_sum()
    except KeyError:
        # This side has humn
        has_humn = 'R'

    # Left side has humn
    if has_humn == 'L':
        value = eval('{}{}{}'.format(value, inverse[monkeys[node].math], R))
        if l == 'humn':
            print("Part 2: {}".format(int(value)))
            exit(0)
        invert(value, l)
    else:
        # If the operation is - and the RHS has humn then we need to subtract the left side from value and invert value
        if monkeys[node].math == '-':
            value = eval('{}{}{}'.format(value, monkeys[node].math, L))
            value = -value
        else:
            value = eval('{}{}{}'.format(value, inverse[monkeys[node].math], L))
        if r == 'humn':
            print("Part 2: {}".format(int(value)))
            exit(0)
        invert(value, r)

# Start with the static side of the root == kid
value = monkeys[monkeys['root'].kids[1]].get_sum()
invert(value, monkeys['root'].kids[0])
