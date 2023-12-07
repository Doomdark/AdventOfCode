password = 'abcdefgh'
password = 'ghijklmn'
password = 'cqjxjnds'

def valid(pw):
    valid = True
    # Check for a triplet
    triplet = 0
    triplet_letter = None
    for c in pw:
        if triplet_letter is None:
            triplet_letter = c
            triplet += 1
        else:
            if triplet < 3:
                if ord(triplet_letter)+1 == ord(c):
                    triplet_letter = c
                    triplet += 1
                else:
                    triplet_letter = c
                    triplet = 1
        if triplet == 3:
            break
    if triplet < 3:
        valid = False

    # Check for i,o,l
    if any([x in pw for x in ['i','o','l']]):
        valid = False

    # Check for at least 2 doubles
    double_count = 0
    double_letter = None
    for c in pw:
        if double_letter is None:
            double_letter = c
        else:
            if c == double_letter:
                double_count += 1
                double_letter = None
            else:
                double_letter = c

    if double_count < 2:
        valid = False

    return valid

def increment(pw):
    npw = ''
    incr = True
    for i in range(len(pw)-1,-1,-1):
        if incr:
            if pw[i] == 'z':
                npw += 'a'
                incr = True
            else: # Next char
                nc = chr(ord(pw[i])+1)
                npw += nc
                incr = False
        else:
            npw += pw[i]
            incr = False

    return npw[::-1]

while not valid(password):
    password = increment(password)

print('Part 1:', password)

password = increment(password)

while not valid(password):
    password = increment(password)

print('Part 2:', password)
