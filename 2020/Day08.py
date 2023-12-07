import copy

instructions = []

with open("Day08_input.txt") as f:
    for line in f.readlines():
        op,arg = line.rstrip().split()
        instructions.append((op,int(arg)))

acc = 0
pc = 0

def run(ins):
    acc = 0
    pc = 0
    executed = {}
    try:
        while (pc not in executed):
            op,arg = ins[pc]
            #print (op,arg)
            executed[pc] = 1
            if op == "acc":
                acc += arg
                pc += 1
            elif op == "jmp":
                pc += arg
            elif op == "nop":
                pc += 1
    except IndexError:
        pass
    return acc,pc

acc,pc = run(instructions)
print ("Part 1:", acc)

for i in range(len(instructions)):
    # Modify the instruction
    instrs = copy.deepcopy(instructions)
    op,arg = instrs[i]

    if op in ['jmp','nop']:
        if op == 'jmp':
            op = 'nop'
        else:
            op = 'jmp'
        instrs[i] = (op,arg)
    else:
        continue

    # Now run the program
    acc,pc = run(instrs)
    if pc == len(instrs):
        break
    
print ("Part 2:", acc)
