lines = open('02.in').read().splitlines()

games = {}

mr,mg,mb = 12,13,14

for line in lines:
    _num, game = line.split(': ')
    num = _num.split()[1]
    turns = game.split('; ')
    views = []
    for turn in turns:
        counts = turn.split(', ')
        r,g,b=0,0,0
        for count in counts:
            number, colour = count.split()
            n = int(number)
            if   colour == 'red':   r = n
            elif colour == 'green': g = n
            elif colour == 'blue':  b = n
        view = (r,g,b)
        views.append(view)
    games[int(num)] = views

# Part 1

id_sum = 0

for game,views in games.items():
    good = True
    for v in views:
        if v[0] > mr or v[1] > mg or v[2] > mb:
            good = False
            break
    if good:
        id_sum += game

print('Part 1:', id_sum)

#  Part 2

power_sum = 0

for game,views in games.items():
    maxr,maxg,maxb = 0,0,0
    for v in views:
        maxr = max(maxr,v[0])
        maxg = max(maxg,v[1])
        maxb = max(maxb,v[2])
    power_sum += (maxr*maxg*maxb)

print('Part 2:', power_sum)

