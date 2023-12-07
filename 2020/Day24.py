colour_swap = {'b':'w', 'w':'b'}

class Tile:
    def __init__(self):
        self.e = None
        self.ne = None
        self.nw = None
        self.w = None
        self.sw = None
        self.se = None
        # Tiles start off as white
        self.colour = 'w'

    def flip(self):
        self.colour = colour_swap[self.colour]

tiles = []
moves = 0

def move(tile,d):
    global moves
    moves += 1
    # Make a new tile
    new_tile = Tile()
    if d == 'e':
        if tile.e is None:
            tile.e = new_tile
            new_tile.w = tile
            tiles.append(new_tile)
        return tile.e
    elif d == 'ne':
        if tile.ne is None:
            tile.ne = new_tile
            new_tile.sw = tile
            tiles.append(new_tile)
        return tile.ne
    elif d == 'se':

        if tile.se is None:
            tile.se = new_tile
            new_tile.nw = tile
            tiles.append(new_tile)
        return tile.se
    elif d == 'w':
        if tile.w is None:
            tile.w = new_tile
            new_tile.e = tile
            tiles.append(new_tile)
        return tile.w
    elif d == 'sw':
        if tile.sw is None:
            tile.sw = new_tile
            new_tile.ne = tile
            tiles.append(new_tile)
        return tile.sw
    elif d == 'nw':
        if tile.nw is None:
            tile.nw = new_tile
            new_tile.se = tile
            tiles.append(new_tile)
        return tile.nw

def process_line(line):
    posn = 0
    d = ''
    # Start at the reference tile
    tile = tiles[0]
    while posn < len(line):
        # If this is a 2-char direction then read that in
        if line.startswith(('e','w'), posn):
            d = line[posn]
            posn += 1
        else:
            d = line[posn:posn+2]
            posn += 1
        # Process the direction
        tile = move(tile,d)

    # Flip the last tile
    tile.flip()
    # Which tile got flipped?
    for c,t in enumerate(tiles):
        if tile == t:
            print("Flipped tile", c)

# Make reference tile
tile = Tile()
tiles.append(tile)

with open("Day24_input.txt") as f:
    lines = f.read().splitlines()
    for line in lines:
        process_line(line)

#print("Moves:", moves)
#print("How many tiles?", len(tiles))
print("Part 1:", ''.join([tile.colour for tile in tiles]).count('b'))
