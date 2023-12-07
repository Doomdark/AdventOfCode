from collections import defaultdict
import math

class Tile:
    def __init__(self, number, image):
        self.number = number
        self.image = image

    def flip(self):
        '''Flips about horizontal line'''
        self.image = list(reversed(self.image))

    def tedge(self):
        '''Top edge'''
        return self.image[0]

    def bedge(self):
        '''Bottom edge'''
        return self.image[-1]

    def ledge(self):
        '''Left edge'''
        return ''.join([x[0] for x in self.image])

    def redge(self):
        '''Right edge'''
        return ''.join([x[-1] for x in self.image])

    def edges(self):
        '''The current edges'''
        return [self.tedge(), self.bedge(), self.ledge(), self.redge()]

    def all_edges(self):
        '''All the edges possible from this tile. So all current edges, and their reversed counterparts.'''
        _all_edges = self.edges()
        return _all_edges + [''.join(reversed(x)) for x in _all_edges]

    def edge_match(self, edge, top=False):
        if top:
            return edge == self.tedge()
        else:
            return edge == self.ledge()

    def rotate(self):
        '''Rotate clockwise'''
        rows = []
        # Iterate through the columns
        for i in range(len(self.image)):
            col = ''.join([x[i] for x in self.image])
            # Add the column as a row
            rows.append(col)
        self.image = list(reversed(rows))

    def strip(self):
        '''Remove the outer border'''
        rows = []
        # For all but the top and bottom rows...
        for i in range(1,len(self.image)-1):
            # Chop each end off the rows
            col = self.image[i][1:-1]
            rows.append(col)
        self.image = rows
        
    def __repr__(self):
        return "\n".join(self.image)

tiles = []

with open("Day20_input.txt") as f:
    number = 0
    tile = []
    for line in f.readlines():
        if line.startswith("Tile"):
            number = int(line.split()[1].split(':')[0])
        elif line.startswith(('.','#')):
            tile.append(line.rstrip())
        else: # End of tile
            t = Tile(number, tile)
            tiles.append(t)
            tile = []

# The jigsaw is square
length = int(math.sqrt(len(tiles)))

# Now try to work out which tiles are in the corners
edge_map = defaultdict(list)
for tile in tiles:
    # For each different edge, append which tiles have those edges. Corners have 2 edges with only 1 instance of that edge.
    for e in tile.all_edges():
        edge_map[e].append(tile.number)

# Now find the corners. Those tiles have only 2 matching edges in all the edge map.
corners = []
for tile in tiles:
    count = 0
    # For each tile edges
    for e in tile.edges():
        count += len(edge_map[e]) - 1 # Each edge appears twice in the list for matches, except for unmatched edges
    if count == 2:
        corners.append(tile)

# Multiply the corner numbers together to get the answer to part 1
print("Part 1:", math.prod([x.number for x in corners]))

# Now we need to place the tiles in the right order in the jigsaw
jigsaw = [[0] * length for x in range(length)]

# Pick a corner. It doesn't matter which one.
active = corners[0]
# Rotate the tile until the left and top edges have edge map entries of only 1
while (len(edge_map[active.ledge()]) == 2) or (len(edge_map[active.tedge()]) == 2):
    active.rotate()

# Assign the top left corner tile in the jigsaw
jigsaw[0][0] = active

# Prevent matching tiles which have already been matched
matched = {}
matched[active.number] = 1

def get_match(source, edge, top=False):
    '''Try all the orientations for matching'''
    # Get the tile from the tile list which has a matching edge for the provided edge. There should only be 1 match.
    tile = [t for t in tiles if edge in t.all_edges() and t.number not in matched][0]
    # Try all 4 rotations to match the provided edge
    for i in range(4):
        tile.rotate()
        if tile.edge_match(edge, top):
            matched[tile.number] = 1
            return tile
    # No matches yet - flip the tile and try again
    tile.flip()
    # Try all 4 rotations to match the provided edge
    for i in range(4):
        tile.rotate()
        if tile.edge_match(edge, top):
            matched[tile.number] = 1
            return tile

    print("Error - no match for", source.number)

# For each row, match the right edge of the previous tile with the left edge of the other tiles.
# Unless it's the first in the row, then match the bottom edge of the tile in the previous (row,0) against the top edge of the other tiles.
# (0,0) is the first corner, already chosen above.
# Iterate over the rows.
for row in range(0,length):
    # Don't do (0,0) because we've already got it.
    if row > 0:
        # First column entry looks for a matching bottom edge of the previous row's tile 0
        previous = jigsaw[row-1][0]
        # Get the matching tile
        tile = get_match(previous, previous.bedge(), True)
        # Add it to the jigsaw
        jigsaw[row][0] = tile

    # For all other elements match the left edge against the right edge of the previous tile
    for col in range(1,length):
        previous = jigsaw[row][col-1]
        # Get the matching tile
        tile = get_match(previous, previous.redge())
        # Add it to the jigsaw
        jigsaw[row][col] = tile

# Make the whole picture

# Remove the borders from each tile first
for i in range(length):
    for j in range(length):
        jigsaw[i][j].strip()

# Now make a composite picture from each tile
pic = []
# Iterate over each row of tiles
for i, row in enumerate(jigsaw):
    # Now iterate over each row in each tile
    for i2 in range(len(row[0].image)):
        s = ''
        for j, col in enumerate(jigsaw[i]):
            s += col.image[i2]
        pic.append(s)

# make a Tile object for the whole picture to make rotation simple
Pic = Tile(0, pic)

# OK, now search for monsters in the picture

MONSTER = """\
                  #
#    ##    ##    ###
 #  #  #  #  #  #   """.split('\n')

# Check all 4 rotations for monsters because we don't know which way round the jigsaw is
for i in range(4):
    # Rotate the whole picture
    Pic.rotate()
    cnt = 0
    for y in range(len(pic)-len(MONSTER)):
        for x in range(len(pic)-len(MONSTER[0])):
            # Check if there's a monster starting at this position
            match = True
            for y0 in range(len(MONSTER)):
                for x0 in range(len(MONSTER[y0])):
                    if MONSTER[y0][x0] == '#' and Pic.image[y+y0][x+x0] != '#':
                        match = False
                        break
                if not match:
                    break
    
            if match:
                cnt += 1
    if cnt:
        break

all_hashes     = ''.join(pic).count('#')
monster_hashes = ''.join(MONSTER).count('#')

print("Part 2:", all_hashes - (monster_hashes*cnt))
