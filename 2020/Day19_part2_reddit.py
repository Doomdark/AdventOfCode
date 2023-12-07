import re
rs, ms = open('Day19_input.txt').read().split('\n\n')
rs += '\n8: 42 | 42 8\n11: 42 31 | 42 11 31' #part 2
rs = dict([line.split(': ') for line in rs.split('\n')])

def f(r='0', n=0):
    if n > 20: return ''
    if rs[r][0] == '"': return rs[r][1]
    return '('+'|'.join([''.join([f(t, n+1) 
        for t in s.split()]) for s in rs[r].split('|')])+')'
           
r = re.compile(f())
print(len([*filter(r.fullmatch, ms.split())]))
