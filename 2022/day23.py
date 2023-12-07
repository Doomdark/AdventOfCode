lines = open("23.in").read().splitlines()

elves = set()

move_order = ['N','S','W','E']

def loc_from_offset(loc,offset):
    x,y = loc
    dx,dy = offset
    nx,ny = x+dx,y+dy
    return (nx,ny)

class Elf:
    def __init__(self,loc):
        self.loc = loc
        self.proposed_move = (None,(0,0))

    def get_adjacent(self,offsets,elf_locs):
        # Iterate through them
        for offset in offsets:
            # Any elves at that location?
            if loc_from_offset(self.loc,offset) in elf_locs:
                return True
        # No adjacent elves
        return False

    def propose_move(self,elf_locs):
        # Check all adjacents locations first
        any_adjacent = False
        offsets = [(-1,-1),(0,-1),(1,-1), # NW, N, NE
                  (-1,1),(0,1),(1,1),     # SW, S, SE
                  (-1,0),                 # W
                  (1,0)]                  # E
        if self.get_adjacent(offsets,elf_locs):
            any_adjacent = True
        # If there are any adjacent elves then try to move
        if any_adjacent:
            # Try moving in the order of the moves
            for move in move_order:
                adjacents = False
                if   move == 'N': offsets = [(-1,-1),( 0,-1),( 1,-1)] # NW, N, NE
                elif move == 'S': offsets = [(-1, 1),( 0, 1),( 1, 1)] # SW, S, SE
                elif move == 'W': offsets = [(-1,-1),(-1, 0),(-1, 1)] # NW, W, SW
                elif move == 'E': offsets = [( 1,-1),( 1, 0),( 1, 1)] # NE, E, SE
                # Check the adjacents
                if self.get_adjacent(offsets,elf_locs):
                    adjacents = True
                # No adjacent elves?
                if not adjacents:
                    if   move == 'N':
                        self.set_proposed_move('N',( 0, -1))
                        return
                    elif move == 'S':
                        self.set_proposed_move('S',( 0, 1))
                        return
                    elif move == 'W':
                        self.set_proposed_move('W',(-1, 0))
                        return
                    elif move == 'E':
                        self.set_proposed_move('E',( 1, 0))
                        return
        self.set_proposed_move(None,(0,0))

    def set_proposed_move(self,d,offset):
        nloc = loc_from_offset(self.loc,offset)
        self.proposed_move = (d,nloc)

    def move(self, destinations):
        # If we're not moving because there's another elf in the way
        d,(nloc) = self.proposed_move
        # Are we moving at all?
        if d is None:
            return False
        # Are there multiple destinations with the same location?
        if destinations.count(nloc) > 1:
            return False
        # Update this elf's location
        self.loc = nloc
        # Say that we moved
        return True

# Make the elves
y = 0
for line in lines:
    for x,char in enumerate(line):
        if char == '#':
            elf = Elf((x,y))
            elves.add(elf)
    y += 1

def draw_grid():
    print('-'*10)
    minx = min([elf.loc[0] for elf in elves])
    maxx = max([elf.loc[0] for elf in elves])
    miny = min([elf.loc[1] for elf in elves])
    maxy = max([elf.loc[1] for elf in elves])
    locs = set([elf.loc for elf in elves])

    for y in range(miny,maxy+1):
        row = ''
        for x in range(minx,maxx+1):
            if (x,y) in locs:
                row += '#'
            else:
                row += '.'
        print(row)

def get_empty_tiles():
    minx = min([elf.loc[0] for elf in elves])
    maxx = max([elf.loc[0] for elf in elves])
    miny = min([elf.loc[1] for elf in elves])
    maxy = max([elf.loc[1] for elf in elves])
    xsize = maxx-minx+1
    ysize = maxy-miny+1
    elf_count = len(elves)
    return xsize*ysize - elf_count

#print(len(elves), 'elves')

moved = True
count = 0
elf_locs = []
while moved:
    elves_moved = 0
    # Next time round
    count += 1
    # No movement by default
    moved = False
    # List of current elf locations
    elf_locs = set([elf.loc for elf in elves])
    # Determine next moves
    for elf in elves:
        elf.propose_move(elf_locs)
    # What are the proposed destinations from all the elves?
    destinations = [elf.proposed_move[1] for elf in elves]
    # Do the moves
    for elf in elves:
        # Move the elf if there's nothing at the destination, and if no other elf is trying to move there
        _moved = elf.move(destinations)
        # Did this elf move?
        if _moved:
            moved = True
            elves_moved += 1
    # update the move order
    move_order = move_order[1:] + move_order[:1]
    # If we're on oloop 10 then print out the empty tile count
    if count == 10:
        print('Part 1:',get_empty_tiles())
    #print('Round',count,'-',elves_moved,'elves moved')

# When did the elves all stop moving?
print('Part 2:',count)
