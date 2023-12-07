rows = []

with open("Day11_input.txt") as f:
    for line in f.readlines():
        rows.append([x for x in line.rstrip()])

dirs = {'N' :{'y':-1,'x':+0},
        'NE':{'y':-1,'x':+1},
        'E' :{'y':+0,'x':+1},
        'SE':{'y':+1,'x':+1},
        'S' :{'y':+1,'x':+0},
        'SW':{'y':+1,'x':-1},
        'W' :{'y':+0,'x':-1},
        'NW':{'y':-1,'x':-1} }

def move(y,x,dirn):
    _y = y + dirs[dirn]['y']
    _x = x + dirs[dirn]['x']
    if _y < 0 or _y >= len(rows) or _x < 0 or _x >= len(rows[0]):
        return (None,None)
    else:
        return (_y, _x)

def get_next_seat(rows,y,x,dirn):
    _y = y
    _x = x
    while (1):
        _y,_x = move(_y,_x,dirn)
        if _y is None:
            return '.'
        else:
            if rows[_y][_x] in ['#','L']:
                return rows[_y][_x]

def check_seat(rows,y,x,check='#'):
    count = 0
    if x-1 >= 0:
        if y-1 >= 0:
            if rows[y-1][x-1] == check: count += 1
        if rows[y][x-1] == check: count += 1
        if y+1 < len(rows):
            if rows[y+1][x-1] == check: count += 1
    if x+1 < len(rows[0]):
        if y-1 >= 0:
            if rows[y-1][x+1] == check: count += 1
        if rows[y][x+1] == check: count += 1
        if y+1 < len(rows):
            if rows[y+1][x+1] == check: count += 1
    if y-1 >= 0:
        if rows[y-1][x] == check: count += 1
    if y+1 < len(rows):
        if rows[y+1][x] == check: count += 1
    return count

def check_seat2(rows,y,x,check='#'):
    count = 0
    if x-1 >= 0:
        if y-1 >= 0:
            if get_next_seat(rows,y,x,'NW') == check: count += 1
        if get_next_seat(rows,y,x,'W') == check: count += 1
        if y+1 < len(rows):
            if get_next_seat(rows,y,x,'SW') == check: count += 1
    if x+1 < len(rows[0]):
        if y-1 >= 0:
            if get_next_seat(rows,y,x,'NE') == check: count += 1
        if get_next_seat(rows,y,x,'E') == check: count += 1
        if y+1 < len(rows):
            if get_next_seat(rows,y,x,'SE') == check: count += 1
    if y-1 >= 0:
        if get_next_seat(rows,y,x,'N') == check: count += 1
    if y+1 < len(rows):
        if get_next_seat(rows,y,x,'S') == check: count += 1
    return count

def makerows(rows,seats):
    newrows = []
    for i in range(rows):
        row=[]
        for j in range(seats):
            row.append('.')
        newrows.append(row)
    return newrows

def num_occupied(rows):
    count = 0
    for row in rows:
        for seat in row:
            if seat == '#':
                count += 1
    return count

#print ('\n'.join([''.join(row) for row in rows]))

def part1(rows):
    while(1):
        newrows = makerows(len(rows),len(rows[0]))
        #print(newrows)
        for row in range(len(rows)):
            for seat in range(len(rows[0])):
                #if row == 1:
                #    print("row", row, "seat", seat)
                if rows[row][seat] == 'L':
                    occupieds = check_seat(rows,row,seat,'#')
                    #print(occupieds)
                    newrows[row][seat] = '#' if occupieds == 0 else 'L'
                elif rows[row][seat] == '#':
                    occupieds = check_seat(rows,row,seat,'#')
                    #if row == 1:
                    #    print ("Occ:", occupieds)
                    newrows[row][seat] = 'L' if occupieds >= 4 else '#'
        #print()                
        #print ('\n'.join([''.join(row) for row in newrows]))
        #End condition
        if rows == newrows:
            print ("Part1:", num_occupied(rows))
            return
            
        rows = newrows
                     
#part1(rows)

def part2(rows):
    while(1):
        newrows = makerows(len(rows),len(rows[0]))
        #print(newrows)
        for row in range(len(rows)):
            for seat in range(len(rows[0])):
                #if row == 1:
                #    print("row", row, "seat", seat)
                if rows[row][seat] == 'L':
                    occupieds = check_seat2(rows,row,seat,'#')
                    #print(occupieds)
                    newrows[row][seat] = '#' if occupieds == 0 else 'L'
                elif rows[row][seat] == '#':
                    occupieds = check_seat2(rows,row,seat,'#')
                    #if row == 1:
                    #    print ("Occ:", occupieds)
                    newrows[row][seat] = 'L' if occupieds >= 5 else '#'
        #print()                
        #print ('\n'.join([''.join(row) for row in newrows]))
        #End condition
        if rows == newrows:
            print ("Part1:", num_occupied(rows))
            return
            
        rows = newrows
                     
part2(rows)
