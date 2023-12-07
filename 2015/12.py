import json

stuff = json.load(open('12.in'))

total = 0

def recurse(node, part2=False):
    global total
    if isinstance(node,dict):
        if part2:
            for v in node.values():
                if isinstance(v,str) and v == 'red':
                    return
        for k,v in node.items():
            # Is the current value a list?
            if isinstance(v, list):
                recurse(v,part2)
            elif isinstance(v,dict):
                recurse(v,part2)
            elif isinstance(v,int):
                total += v
            # Ignore strings
    elif isinstance(node,list):
        for item in node:
            if isinstance(item, int):
                total += item
            elif isinstance(item, dict):
                recurse(item,part2)
            elif isinstance(item, list):
                recurse(item,part2)

recurse(stuff)
print('Part 1:', total)

total = 0
recurse(stuff,True)
print('Part 2:', total)
