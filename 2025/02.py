# Read the input
line = open("02.in").read()

ranges = line.split(',')

invalid = 0

for RANGE in ranges:
    l,r = [int(x) for x in RANGE.split('-')]
    for i in range(l,r+1):
        str_i = str(i)

        if len(str_i) %2 == 0:
            L = str_i[:len(str_i)//2]
            R = str_i[len(str_i)//2:]

            if L == R:
                invalid += i

print('Part 1:', invalid)

invalid = 0

def getSubStrings(s, l):
    return [s[i:i+l] for i in range(0, len(s), l)]

def try_match(str_i):
    for l in range(1,len(str_i)+1):
        matches = 0
        mismatch = False
        strings = getSubStrings(str_i, l)
        if len(strings) == 1:
            continue
        if len(str_i)%len(strings[0]) > 0 :
            continue
        #print('%%',strings)
        for thing in strings[1:]:
            if thing == strings[0]:
                matches += 1
            else:
                mismatch = True

        if not mismatch and matches >= 1:
            print(strings, matches)
            print('*', i)
            return i
    return 0

for RANGE in ranges:
    l,r = [int(x) for x in RANGE.split('-')]
    for i in range(l,r+1):
        str_i = str(i)
        invalid += try_match(str_i)

print('Part 2:', invalid)
