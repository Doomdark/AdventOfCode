# Read the input
lines = open("07.in").read().splitlines()

# Make a dictionary of beams
beams = {}

# Read in the location of the beam start
beams[lines[0].index('S')] = 1

# Count the splits for part 1
splits = 0

# Go down the rows and split the beams at the splitter points
for row in lines:
    # New beams dictionary for this step
    nbeams = {}
    # Test each beam
    for c in beams:
        # Hit a splitter
        if row[c] == '^':
            # Count the splits for part 1
            splits += 1
            # Add two beams to the new beams dictionary
            # Sum the number of beams at each location for part 2
            nbeams[c-1] = nbeams.get(c-1,0) + beams[c]
            nbeams[c+1] = nbeams.get(c+1,0) + beams[c]
        else: # Beam doesn't split so add it to the new beams dictionary
            nbeams[c] = nbeams.get(c,0) + beams[c]
    # Store new beams for the next iteration
    beams = nbeams

print('Part 1:', splits)
print('Part 2:', sum([x for x in beams.values()]))
