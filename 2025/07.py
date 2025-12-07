# Read the input
lines = open("07.in").read().splitlines()

# Make a set of splitters
splitters = set()
beams = {}

# Read in the location of the beam start and the splitters
for r,line in enumerate(lines):
    for c,char in enumerate(line):
        # Store the splitter locations
        if char == '^': splitters.add((r,c))
        # Only one beam exists initially
        elif char == 'S': beams[(r,c)] = 1

# Count the splits for part 1
splits = 0

# Go down the list and split the beams at the splitter points
for i in range(len(lines)-1):
    # New beams dictionary for the next step
    nbeams = {}
    # Test each beam
    for (r,c) in beams:
        # New beam moves downwards
        nr = r+1
        # New default beam location
        nbeam = (nr,c)
        # Is this a splitter location?
        if nbeam in splitters:
            # Count the splits for part 1
            splits += 1
            # Two new beams
            nbeaml = (nr,c-1)
            nbeamr = (nr,c+1)
            # Add to the new beams dictionary
            # Sum the number of beams at each location for part 2
            nbeams[nbeaml] = nbeams.get(nbeaml,0) + beams[(r,c)]
            nbeams[nbeamr] = nbeams.get(nbeamr,0) + beams[(r,c)]
        else: # Beam doesn't split so add it to the new beams dictionary
            nbeams[nbeam] = nbeams.get(nbeam,0) + beams[(r,c)]
    # Store new beams for the next iteration
    beams = nbeams

print('Part 1:', splits)
print('Part 2:', sum([x for x in beams.values()]))
