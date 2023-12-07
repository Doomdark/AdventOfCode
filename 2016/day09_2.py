from itertools import takewhile, islice

def decompress(data, recurse):
    answer = 0
    chars = iter(data)
    for c in chars:
        if c == '(':
            n, m = map(int, [''.join(takewhile(lambda c: c not in 'x)', chars)) for _ in (0, 1)])
            s = ''.join(islice(chars, n))
            answer += (decompress(s, recurse) if recurse else len(s))*m
        else:
            answer += 1
    return answer

data = open('day09_input.txt').read().strip()
print('Answer #1:', decompress(data, False))
print('Answer #2:', decompress(data, True))
