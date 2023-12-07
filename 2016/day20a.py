maximum = 4294967295
ranges = []

def day20a(d):
    global ranges
    d = d.strip().split('\n')
    for ips in d:
        rang = ips.split('-')
        rang[0],rang[1] = int(rang[0]),int(rang[1])
        ranges.append(rang)
    ranges = sorted(ranges, key=lambda x: x[0])
    used = 0
    for rang in ranges:
        if rang[0] <= used + 1:
            used = max(rang[1], used)
        else:
            return used + 1
    return -1 if used == maximum else maximum

def day20b(d):
    global ranges, maximum
    used = 0
    count = 0
    for rang in ranges:
        if rang[0] > used + 1:
            count += rang[0] - used - 1
        used = max(rang[1], used)
    count += maximum - used
    return count

with open('20.in') as f:
    day20a(f)
    day20b(f)
    
