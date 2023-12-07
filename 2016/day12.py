regs = {'a':0, 'b':0, 'c':1, 'd':0}

instrs = [
    "cpy 41 a",
    "inc a",
    "inc a",
    "dec a",
    "jnz a 2",
    "dec a"
    ]

with open("day12_input.txt") as f:
    for line in f.readlines():
        instrs.append(line.rstrip())

i = 0
while i < len(instrs):
    l = instrs[i].split()
    if l[0] == "cpy":
        src = None
        if l[1].isdigit():
            src = int(l[1])
        else:
            src = regs[l[1]]
        regs[l[2]] = src
        i += 1
    elif l[0] == "inc":
        regs[l[1]] += 1
        i += 1
    elif l[0] == 'dec':
        regs[l[1]] -= 1
        i += 1
    elif l[0] == 'jnz':
        if l[1].isdigit():
            test = int(l[1])
        else:
            test = regs[l[1]]
        if test != 0:
            i += int(l[2])
        else:
            i += 1

print("Part 1:", regs['a'])
