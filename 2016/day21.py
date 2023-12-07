import copy
from collections import deque
import itertools

password = 'abcdefgh'

insts = open('21.in').read().splitlines()

def scrambler(word, instructions, part2=False):
    begin = ''.join(word)
    for inst in instructions:
        instsplit = inst.split(' ')
        if instsplit[0] == 'rotate':
            if instsplit[1] == 'based':
                amount = word.index(instsplit[6])
                if amount >= 4:
                    amount += 1
                amount += 1
            else:
                amount = int(instsplit[2])
            wordsplit = deque([x for x in word])
            if instsplit[1] in ['based', 'right']:
                wordsplit.rotate(amount)
                word = ''.join(wordsplit)
            if instsplit[1] == 'left':
                wordsplit.rotate(-amount)
                word = ''.join(wordsplit)
        elif instsplit[0] == 'swap':
            if instsplit[1] == 'letter':
                a = word.index(instsplit[2])
                b = word.index(instsplit[5])
            elif instsplit[1] == 'position':
                a = int(instsplit[2])
                b = int(instsplit[5])
            newa = copy.copy(word[a])
            newb = copy.copy(word[b])
            word = word[:a] + newb + word[a+1:]
            word = word[:b] + newa + word[b+1:]
        elif instsplit[0] == 'move':
            a = int(instsplit[2])
            b = int(instsplit[5])
            temp = copy.copy(word[a])
            word = word[:a] + word[a+1:]
            word = word[:b] + temp + word[b:]
        elif instsplit[0] == 'reverse':
            lo = int(instsplit[2])
            hi = int(instsplit[4])
            word = word[:lo] + ''.join(reversed(word[lo:hi+1])) + word[hi+1:]

    if part2:
        if word == 'fbgdceah':
            return begin
        else:
            return None
    else:
        return word
            
print('Part 1:', scrambler('abcdefgh', insts))

# Part 2

# Try all permutations of the password and when the scrambled
# result is the one we want then the initial password is correct.
for word in itertools.permutations(password):
    result = scrambler(word, insts, True)
    if result is not None:
        print('Part 2:', result)
      
