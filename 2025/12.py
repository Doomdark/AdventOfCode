from collections import defaultdict
import copy

Pieces = {}
Regions = []

# Read the input
lines = open("12a.in").read().splitlines()

index = None

for line in lines:
    if 'x' in line:
        r,q = line.split(': ')
        x,y = [int(a) for a in r.split('x')]
        Regions.append( ((x,y), [int(x) for x in q.split()]) )
    # New piece
    elif ':' in line:
        index = int(line[:-1])
        r = 0
        piece = []
    elif '#' in line:
        for c,char in enumerate(line):
            if char == '#':
                piece.append((r,c))
        r += 1
    else:
        Pieces[str(index)] = tuple(piece)

#print(Regions)
print(Pieces)

def mirrorv(piece):
    'Mirror in a vertical line.'
    # For each location invert the column number, then shift everything right by abs(max col).
    p = []
    maxc = max([c for r,c in piece])
    for r,c in piece:
        p.append((r,-c+maxc))
    return tuple(sorted(p))

def mirrorh(piece):
    'Mirror in a horizontal line.'
    # For each location invert the row number, then shift everything down by abs(max row).
    p = []
    maxr = max([r for r,c in piece])
    for r,c in piece:
        p.append((-r+maxr,c))
    return tuple(sorted(p))

def mirrord(piece):
    'Mirror in a diagonal line going from top left to bottom right.'
    # Swap the r and c coordinates
    p = []
    for r,c in piece:
        p.append((c,r))
    return tuple(sorted(p))

def get_all_orientations(piece):
    'Find all the possible orientations of the provided piece'
    p = {piece}
    p.add(_piece := mirrorv(piece))
    p.add(_piece := mirrorh(_piece))
    p.add(_piece := mirrorv(_piece))
    p.add(_piece := mirrord(_piece))
    p.add(_piece := mirrorv(_piece))
    p.add(_piece := mirrorh(_piece))
    p.add(_piece := mirrorv(_piece))
    return p

def get_all_positions(piece):
    'Get the piece shapes shifted up/down/left/right to cover all possible offsets within the shape.'
    maxr = max([r for r,c in piece])
    maxc = max([c for r,c in piece])
    p = set()
    for r in range(maxr+1):
        for c in range(maxc+1):
            _piece = []
            for (dr,dc) in piece:
                nr,nc = dr-r,dc-c
                _piece.append((nr,nc))
            p.add(tuple(sorted(_piece)))
    return p

def next_free_loc(loc, board):
    'Get the next square (in reading order) that is not occupied.'
    sr,sc = loc
    started = False
    R,C = len(board), len(board[0])
    for r in range(R):
        if not started and r < sr: continue
        for c in range(C):
            if not started and c < sc: continue
            started = True
            if free_loc((r,c), board):
                return (r,c)

def free_loc(loc, board):
    'Is this location available to put a shape on?'
    r,c = loc
    if 0<=r<len(board) and 0<=c<len(board[0]):
        if board[r][c] not in list(PIECES.keys()):
            return True
    return False

PIECES = defaultdict(list)

# Make a dictionary with all the piece orientations in it for each shape
for name,piece in Pieces.items():
    # For all of those orientations get the up/down/left/right shifted positions
    for orientation in get_all_orientations(piece):
        PIECES[name].extend(get_all_positions(orientation))

def print_board(board, it):
    print('---', it)
    for x in range(len(board)):
        print(board[x])

def solve(loc, board, pieces):

    def dfs(_loc, _board, _pieces, it=0):
        'Try to fit the remaining pieces onto the provided board.'
        r,c = _loc
        print_board(_board, it)
        # Try each piece in turn
        for name in _pieces:
            orientations = PIECES[name]
            # Try to place the piece on the board
            for locs in orientations:
                good = True
                # Make a copy of the board for this new piece orientation test
                __board = copy.deepcopy(_board)
                # Test each of the piece locations for being on the board
                for dr,dc in locs:
                    nr,nc = r+dr,c+dc
                    # Piece outside of the board boundary or already occupied?
                    if not free_loc((nr,nc), __board):
                        good = False
                        break
                    # Place the piece into the location
                    __board[nr][nc] = name
                # This orientation didn't work, try the next one
                if not good:
                    continue
                else: # The piece fitted OK
                    # If there are remaining pieces then try the next one
                    if len(_pieces) > 1:
                        remaining_pieces = _pieces[1:]
                        # Find the next free board square to place a piece
                        nr,nc = next_free_loc((0,0), __board)
                        dfs((nr,nc), __board, remaining_pieces, it+1)
                    else: # Finished! Print out the board
                        return 1

            # The piece didn't fit, try the next one
        # None of the pieces fitted. Go back to Old Kent Road
        return 0

    return dfs(loc, board, pieces)

# How many of each piece do we want to try to fit in?
i = 0
fits = 0
for size, quantities in Regions:
    all_pieces = []
    board = [(['.']*size[1]) for _ in range(size[0])]
    for a,num in enumerate(quantities):
        if num > 0:
            for b in range(num):
                all_pieces.append( str(a) )
    i+=1
    print( solve((0,0), board, all_pieces) )
    break

print('Part 1:', fits)

#l = list(PIECES.items())
#PIECES = dict(l)

#solve((0,0), G, PIECES)
