import re

lines = open('04.in').read().splitlines()

# Part 1

part1 = 0

cards = {}

for line in lines:
    matches = 0
    worth = 0
    # Split the lines up
    a,b = line.split(' | ')
    c,d = a.split(': ')
    card,num = c.split()
    # Find all the numbers
    winning_nums = re.findall('\d+', d)
    my_nums = re.findall('\d+', b)
    # Process the numbers
    for n in my_nums:
        if n in winning_nums:
            matches += 1
            worth = 1 if worth == 0 else worth * 2
    # Accumulate the worth for part 1
    part1 += worth
    # Store the match count of each card for part 2
    cards[int(num)] = {'matches':matches, 'count':1}

print('Part 1:', part1)

# Part 2

for num, card in cards.items():
    # Does this card have at least one match?
    if card['matches'] > 0:
        extras = card['count']
        # Add on the duplicates for the other cards
        for i in range(1,card['matches']+1):
            # Ignore out of range cards
            try:
                cards[num+i]['count'] += extras
            except KeyError:
                pass

# Sum all the card counts
part2 = sum([c['count'] for k,c in cards.items()])
print('Part 2:', part2)
