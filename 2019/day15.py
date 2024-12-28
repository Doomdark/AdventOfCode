import sys
sys.path.append('/home/rwilkinson/Python')

from intcode import Intcode
from collections import defaultdict
import networkx as nx

# Make a graph to store the maze into
G = nx.Graph()

# Program memory
program = defaultdict(int)

# Read the intcode program
#with open("day15_input.txt",'r') as f:
#    for line in f.readlines():
#        for i,x in enumerate(line.rstrip().split(',')):
#            program[i] = int(x)

program.update({i:int(x) for i,x in enumerate(open("day15_input.txt").read().rstrip().split(','))})

# Run the computer
c = Intcode(program)
c.start()

# Opposite direction map
opposite = {1:2, 2:1, 3:4, 4:3}

# Droid class
class Droid:
    def __init__(self, c, grid, G):
        self.x = 0
        self.y = 0
        self.direction = 1
        self.grid = grid
        self.c = c
        self.G = G
        self.grid[self.coords] = '.'
        self.blocked = defaultdict(int)
        self.deadend = defaultdict(int)
        self.last_coords = None
        self.o2 = None

    @property
    def coords(self):
        return (self.x,self.y)

    def draw_grid(self):
        max_x = 0
        max_y = 0
        min_x = 0
        min_y = 0

        # How big is the grid?
        for x,y in self.grid.keys():
            if x > max_x: max_x = x
            if x < min_x: min_x = x
            if y > max_y: max_y = y
            if y < min_y: min_y = y

        maze = '='*50 + '\n\n'

        for y in range(min_y, max_y+1):
            row = ''
            for x in range(min_x, max_x+1):
                if (x,y) in self.grid:
                    if (x,y) == self.coords:
                        row += 'D'
                    elif (x,y) == (0,0):
                        row += "S"
                    else:
                        row += self.grid[(x,y)]
                else:
                    row += ' '
            maze += row + '\n'

        print(maze + '\n')

    def next_coord(self, direction):
        if   direction == 1: coord = (self.x+1, self.y)
        elif direction == 2: coord = (self.x-1, self.y)
        elif direction == 3: coord = (self.x,   self.y-1)
        else:                coord = (self.x,   self.y+1)
        return coord

    def map_adjacent(self):
        not_blocked = []
        # Move once in each direction and map the squares
        for d in range (1,5):
            # What would the next coord be for this direction?
            nc = self.next_coord(d)

            # Skip any blocked or deadend coords
            if nc in self.blocked: continue
            if nc in self.deadend: continue

            # Move the droid if we know the square isn't blocked
            self.c.put(d)
            status = self.c.get()

            # Look at the resulting status
            if status == 0: # Wall
                self.grid[nc] = '#'
                self.blocked[nc] = 1 # Mark as blocked
                # No movement
            elif status > 0: # A space or the Oxygen Generator
                self.grid[nc] = '.' if status == 1 else 'O'
                # Add a graph edge as we moved
                self.G.add_edge(self.coords, nc)
                # Move back to where we were
                self.c.put(opposite[d])
                # Ignore the new status
                status = self.c.get()
                # Add to the list of unblocked directions
                not_blocked.append(d)

        # If there's only one available exit then this location is a dead end
        if len(not_blocked) == 1:
            self.deadend[self.coords] = 1
        else: # More than one exit
            for d in not_blocked:
                # Don't retreat unnecessarily
                if self.last_coords == self.next_coord(d):
                    not_blocked.remove(d)
                    break

        return not_blocked

    def move(self):
        # Map all the adjacent squares and work out where we can next move to
        adjacents = self.map_adjacent()

        # If there are no more locations to move return with the O2 location
        if len(adjacents) == 0:
            return self.o2

        # Continue forward if we can
        if self.direction in adjacents:
            next_direction = self.direction
        else: # Otherwise choose the first adjacent available location in the list
            next_direction = adjacents[0]

        # Store our current direction
        self.direction = next_direction

        # Store where we currently are
        self.last_coords = self.coords

        # Move the droid in the chosen next direction.
        self.c.put(next_direction)

        # Wait for the status although we know what it will be
        status = self.c.get()

        # Whatever happened we're at the new coordinate
        coord = self.next_coord(next_direction)

        # Update our location
        self.x, self.y = coord

        # Draw the current maze
        self.draw_grid()

        # Store where the oxygen station is when we find it
        if self.grid[self.coords] == 'O':
            self.o2 = self.coords

        return None

# Store some coordinates for the maze
grid = defaultdict(int)

d = Droid(c, grid, G)

while True:
    # Move the droid in the direction it is facing
    loc = d.move()
    if loc is not None:
         x, y = loc
         # Shortest path to oxygen:
         shortest = nx.dijkstra_path_length(G, (0,0), loc)
         print("Part 1: {}".format(shortest))
         # Part 2 requires working out the shortest path to each node from the O2 and then finding the longest of those
         print("Part 2:", max([nx.dijkstra_path_length(G, loc, node) for node in G.nodes]))
         break
