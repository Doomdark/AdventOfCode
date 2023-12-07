from collections import deque
import sys, pickle
cup_string = '389125467'
cup_string = '716892543'
cups = deque()
for char in cup_string:
    cups.append(int(char))

def print_cups(cups):
    print(', '.join(['{}'.format(x) for x in cups]))

def part1(cups):
    # Rotate the list until #0 = 1
    cups.rotate(cups.index(1)*-1)
    print("Part 1:", ''.join(['{}'.format(x) for x in cups if x != 1]))

def part2(cups):
    # Rotate the list until #0 = 1
    cups.rotate(cups.index(1)*-1)
    print("Part 2:", cups[1] * cups[2])

min_label = min(cups)
max_label = max(cups)

repeats = {}

def play(moves):
    move = 0
    while move < moves:
        #print_cups(cups)
        # Rotate to position 0
        current = cups[0]
        cups.rotate(-1)
        # Pick up the next 3 cups
        pickup = []
        for i in range(3):
            pickup.append(cups.popleft())
        #print_cups(pickup)
        # The destination cup is the one lower than the current cup
        destination = current-1
        # Wrap back to the max if we're off the bottom
        if destination < min_label:
            destination = max_label
        #print(current)
        # Unless it's picked up, then subtract a number until it isn't in the pickup
        while destination in pickup:
            destination -= 1
            if destination < min_label:
                destination = max_label
                #sys.exit()
        # Get the list index of the destination and add 1
        #print(destination)
        insert_at = cups.index(destination)+1
        #print("insert_at",insert_at)
        # Add the picked-up cups back into the list
        for i in range(len(pickup)):
            cups.insert(insert_at+i, pickup[i])

        if pickle.dumps(cups) in repeats:
            last_repeat = repeats[pickle.dumps(cups)]
            difference = move - last_repeat
            repeats[pickle.dumps(cups)] = move
            move += ((moves-move) / difference) 
        else:
            repeats[pickle.dumps(cups)] = move
        
        move += 1
play(100)
part1(cups)

cups = deque()
for char in cup_string:
    cups.append(int(char))
    
add = max(cups)
while add < 1000000:
    add += 1
    cups.append(add)

play(10000000)
part2(cups)
