from collections import defaultdict

lines = open('07.in').read().splitlines()

def process(lines, b_override=None):
    wires = defaultdict(int)
    done = False
    while not done:
        # Store the unprocessed lines
        unprocessed_lines = []
        # Iterate through the current set of lines
        for line in lines:
            l = line.split(' -> ')
            lhs = l[0].split()
            rhs = l[1]
            if len(lhs) == 1:
                try:
                    # Try to get an integer
                    if rhs == 'b' and b_override is not None:
                        val = b_override
                    else:
                        val = int(lhs[0])
                except:
                    # Check if the wire exists
                    if lhs[0] in wires:
                        val = wires[lhs[0]]
                    else: # Doesn't exist - try this line again next time
                        unprocessed_lines.append(line)
                        continue
                wires[rhs] = val & 0xFFFF
            elif len(lhs) == 2:
                try:
                    # Try to get an integer
                    val = int(lhs[1])
                except:
                     if lhs[1] in wires:
                         val = wires[lhs[1]]
                     else:
                         unprocessed_lines.append(line)
                         continue
                wires[rhs] = ~val & 0xFFFF
            elif len(lhs) == 3:
                op = lhs[1]
                try:
                    lval = int(lhs[0])
                except:
                    if lhs[0] in wires:
                        lval = wires[lhs[0]]
                    else:
                        unprocessed_lines.append(line)
                        continue
                try:
                    rval = int(lhs[2])
                except:
                    if lhs[2] in wires:
                        rval = wires[lhs[2]]
                    else:
                        unprocessed_lines.append(line)
                        continue
                if   op == 'AND'   : wires[rhs] = (lval &  rval) & 0xFFFF
                elif op == 'LSHIFT': wires[rhs] = (lval << rval) & 0xFFFF
                elif op == 'RSHIFT': wires[rhs] = (lval >> rval) & 0xFFFF
                elif op == 'OR'    : wires[rhs] = (lval |  rval) & 0xFFFF

        if unprocessed_lines == []:
            done = True
        else:
            lines = unprocessed_lines

    return(wires['a'])

part1 = process(lines)
print('Part 1:', part1)
part2 = process(lines, part1)
print('Part 2:', part2)
