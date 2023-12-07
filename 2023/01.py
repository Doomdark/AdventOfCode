lines = open("01.in").read().splitlines()

total = 0

for line in lines:
    a = []
    for i in line:
        try:
            c = int(i)
            a.append(c)
        except:
            pass

    b = a[0]
    c = a[-1]
    total += int('{}{}'.format(b,c))

print('Part 1:',total)

# Part 2

lines = open("01.in").read().splitlines()

nums = {'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,
        'ten':10,'eleven':11,'twelve':12,'thirteen':13,'fourteen':14,'fifteen':15,'sixteen':16,
        'seventeen':17,'eighteen':18,'nineteen':19,'twenty':20,
        '0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}

total = 0
for line in lines:
    first = (None,'0')
    last  = (None,'0')
    for num in sorted(nums.keys(),key=len, reverse=True):
        if num in line:
            f_posn = line.index(num)
            l_posn = line.rfind(num)
            fposn, fnum = first
            lposn, lnum = last
            if fposn is None or f_posn < fposn:
                first = (f_posn, nums[num])
            if lposn is None or l_posn > lposn:
                last = (l_posn, nums[num])

    #print(first[1], last[1])
    b = '{}'.format(first[1])[0]
    c = '{}'.format(last[1])[-1]
    total += int('{}{}'.format(b,c))

print('Part 2:', total)

