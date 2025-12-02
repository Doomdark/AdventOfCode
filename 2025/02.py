# Read the input
line = open("02.in").read()

ranges = line.split(',')

invalid = 0

# Iterate over the ranges
for RANGE in ranges:
    # Get the extents
    l,r = [int(x) for x in RANGE.split('-')]
    # Iterate over this range
    for i in range(l,r+1):
        str_i = str(i)
        # if the length isn't even then it's not a match
        if len(str_i) %2 == 0:
            # Split the string in 2
            L = str_i[:len(str_i)//2]
            R = str_i[len(str_i)//2:]
            # if the two match then that's a win
            if L == R:
                invalid += i

print('Part 1:', invalid)

invalid = 0

def get_substrings(s, l):
    return [s[i:i+l] for i in range(0, len(s), l)]

def try_match(str_i):
    # Try to match patterns of length 1,2,3...
    for l in range(1,len(str_i)):
        # Split strings into equal lengths
        strings = get_substrings(str_i, l)
        # Only 1 string means we've gone past halfway
        if len(strings) == 1:
            return 0
        # Check all the strings in the list are the same
        matches = set(strings)
        # If there's only one set element then that's a match
        if len(matches) == 1:
            return i
    return 0

# Iterate over the ranges
for RANGE in ranges:
    l,r = [int(x) for x in RANGE.split('-')]
    # Iterate over the l->r range
    for i in range(l,r+1):
        str_i = str(i)
        # Try to match patterns in the current string
        invalid += try_match(str_i)

print('Part 2:', invalid)
