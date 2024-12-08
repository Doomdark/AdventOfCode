from collections import defaultdict

lines = open('08.in').read().splitlines()

# List of nodes
nodes = defaultdict(list)

# A list of all occupied nodes
allnodes = {}

for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if char != '.':
            nodes[char].append((r,c))
            allnodes[(r,c)] = char

max_r = len(lines)-1
max_c = len(lines[0])-1

def on_grid(loc):
    r,c = loc
    if r<0 or r>max_r: return False
    if c<0 or c>max_c: return False
    return True

def print_grid(antinodes):
    global allnodes
    for r in range(max_r+1):
        l = ''
        for c in range(max_c+1):
            if (r,c) in allnodes.keys(): l += (allnodes[(r,c)])
            elif (r,c) in antinodes: l += '#'
            else: l+= '.'
        print(l)

# Find antinodes first by looking at pairs of nodes
def solve(nodes, part2=False):
    antinodes = set()
    seen = set()
    for name, _nodes in nodes.items():
        for a in _nodes:
            for b in _nodes:
                # Don't test a point against itself
                if a == b: continue
                # Don't test pairs we've already tested
                id = '_'.join(sorted([str(a),str(b)]))
                if id in seen: continue
                seen.add(id)
                # Determine the distance to go off in each direction
                ar,ac = a
                br,bc = b
                brgar = False
                bcgac = False
                if br >= ar:
                    dr = br-ar
                    brgar = True
                else:
                    dr = ar-br
                if bc >= ac:
                    dc = bc-ac
                    bcgac = True
                else:
                    dc = ac-bc
                # Add the location pairs for part 2
                if part2:
                    antinodes.add(a)
                    antinodes.add(b)
                # Antinodes go off to infinity in part 2
                while(True):
                    # Work out the point differences
                    if brgar:
                        nar = ar-dr
                        nbr = br+dr
                    else:
                        nar = ar+dr
                        nbr = br-dr
                    if bcgac:
                        nac = ac-dc
                        nbc = bc+dc
                    else:
                        nac = ac+dc
                        nbc = bc-dc
                    # Next locations for the pairs
                    na = (nar,nac)
                    nb = (nbr,nbc)
                    # Add antinodes if they're on the grid
                    if on_grid(na): antinodes.add(na)
                    if on_grid(nb): antinodes.add(nb)
                    # Exit here if we're off the grid, or it's part 1
                    if part2:
                        # Stop making antinodes if both directions are off the grid
                        if not on_grid(na) and not on_grid(nb):
                            break
                    # Only one pair of antinodes for part 1
                    else:
                        break
                    # Next locations for part 2
                    ar,ac = na
                    br,bc = nb
    return antinodes

#print_grid(solve(nodes, True))
print('Part 1:', len(solve(nodes)))
print('Part 2:', len(solve(nodes, True)))
