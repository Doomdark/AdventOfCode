from collections import defaultdict, deque
import re

lines = open('19.in').read().splitlines()

subs = defaultdict(list)
string = None

for line in lines:
    if '=>' in line:
        l = line.split(' => ')
        subs[l[0]].append(l[1])
    elif line != '':
        string = line

def solve(subs, string):
    new_strings = set()

    for find in subs.keys():
        if find in string:
            # At what indices are all the matches?
            iter = re.finditer(find, string)
            indices = [m.start(0) for m in iter]
            # Do a replacement for all the occurrences, one at a time
            for index in indices:
                lsb = index
                msb = index+len(find)
                # Do the replacements one by one
                for sub in subs[find]:
                    new_string = string[:lsb] + sub + string[msb:]
                    new_strings.add(new_string)

    return new_strings

print('Part 1:', len(solve(subs,string)))

## Part 2 ##

# Do a BFS with all the possible replacements but in reverse

def solve2(subs, string):
    new_strings = set()

    for sub,vals in subs.items():
        # For each value try to substitute
        for find in vals:
            if find in string:
                # At what indices are all the matches?
                iter = re.finditer(find, string)
                indices = [m.start(0) for m in iter]
                # Do a replacement for all the occurrences, one at a time
                for index in indices:
                    lsb = index
                    msb = index+len(find)
                    # Do the replacements one by one
                    new_string = string[:lsb] + sub + string[msb:]
                    new_strings.add(new_string)

    return new_strings

from heapq import heappush, heappop

q = deque()
q.append((string, 0))

target = 'e'
visited = set()

while q:
    #print(len(q))
    lstring, steps = q.pop()

    # Do all possible replacements
    for _string in list(solve2(subs, lstring)):
        if _string == target:
            print("Part 2:", steps+1)
            exit(0)
        # Add the new string to the list
        if _string not in visited:
            q.append((_string, steps+1))
            visited.add(_string)
