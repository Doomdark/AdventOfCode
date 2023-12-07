passphrases = open("4.in").read().splitlines()

valids = []
for phrase in passphrases:
    pl = phrase.split()
    ps = set(pl)
    if len(pl) == len(ps):
        valids.append(phrase)

print('Part 1:', len(valids))

valids = []
for phrase in passphrases:
    pl = phrase.split()
    ps = set([''.join(sorted(x)) for x in pl])
    if len(pl) == len(ps):
        valids.append(phrase)

print('Part 2:', len(valids))
