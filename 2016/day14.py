from hashlib import md5
import sys

salt = 'zpqevtbw'
#salt = 'abc'

hashes = []
possibles = {}
actuals = []

# Make all the hashes
#for i in range(23729):
#    s = salt + str(i)
#    h = str(md5(s.encode('utf-8')).hexdigest()).lower()
#    hashes.append(h)

def get_hash(i, salt, iterations):
    h = salt + str(i)
    for i in range(iterations):
        h = str(md5(h.encode('utf-8')).hexdigest()).lower()
    return h

i = 0
part2 = True

# Look through the hashes to see if there are any keys
#for index,h in enumerate(hashes):
while True:

    # Make a new hash
    h = get_hash(i, salt, 2017 if part2 else 1)
    #s = salt + str(i)
    #h = str(md5(s.encode('utf-8')).hexdigest()).lower()

    # For all existing possibles, check if the char appears 5 times in a row in the current hash
    new_possibles = {}
    for _index,value in sorted(possibles.items()):
        letter,count = value
        if letter*5 in h:
            actuals.append(_index)
            if len(actuals) == 64:
                print("Part {}:".format('2' if part2 else '1'), _index)
                #print(actuals)
                sys.exit()
        else:
            # Still got iterations left
            if count-1 > 0:
                new_possibles[_index] = (letter, count-1)
    possibles = new_possibles

    # Check if there might be new keys in this new hash
    letters = list(set(h))
    lsb_posn = 100000
    lsb_char = ''
    #if i in [92, 200]:
    #    print(i, h)
    for l in letters:
        if l*3 in h:
            posn = h.index(l*3)
            if posn <= lsb_posn:
                lsb_posn = posn
                lsb_char = l
    # The first triplet matched is the possible character
    if lsb_char != '':
        possibles[i] = (lsb_char, 1000)

    # Next index
    i += 1

    #if i == 818:
    #    break

#print(len(possibles))
#print(len(actuals))
#print('Possibles')
#for p,v in sorted(possibles.items()):
#    print(p, v)
#print('Actuals')
#for v in sorted(actuals):
#    print(v)

#for index,value in sorted(possibles.items()):
