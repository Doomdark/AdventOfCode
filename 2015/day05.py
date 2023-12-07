vowels = set()
vowels.update('a','e','i','o','u')
invalid = ['ab','cd','pq','xy']

strings = ['ugknbfddgicrmopn']
strings = []

with open("day05_input.txt") as f:
    for line in f.readlines():
        strings.append(line.strip())

#strings = ['dvszwmarrgswjxmb']
#strings = ['haegwjzuvuyypxyu']
#strings = ['jchzalrnumimnmhp']
#strings = ['aaa']

def check_repeat(s):
    for i in range(0,len(s)-1):
        if s[i] == s[i+1]:
            return True
    return False

def check_good(s):
    has_3_vowels = len(''.join(filter(None,[x for x in s if x in vowels]))) >= 3
    has_repeat = check_repeat(s)
    has_no_invalid = not any([x in s for x in invalid])
    return has_3_vowels and has_repeat and has_no_invalid

count = 0
for string in strings:
    count += 1 if check_good(string) else 0

print("Part 1:", count)

def check_repeat2(s):
    c0 = None
    c1 = None
    for i in range(0,len(s)-1):
        if c0 is None:
            c0 = str(s[i])
        elif c1 is None:
            c0 = str(s[i-1])
            c1 = str(s[i])
        else:
            check = ''.join([c0,c1])
            # Does this string appear at least twice in the provided string?
            splits = s.split(check)
            if len(splits) > 2:
                return True

            c0 = str(s[i-1])
            c1 = str(s[i])
    return False

def check_repeat3(s):
    for i in range(0,len(s)-2):
        if s[i] == s[i+2]:
            return True
    return False

#strings = ['qjhvhtzxzqqjkmpb']
#strings = ['xxyxx']
#strings = ['uurcxstgmygtbstg']
#strings = ['ieodomkazucvgmuy']
count = 0
for string in strings:
    #print(check_repeat2(string), check_repeat3(string))
    count += 1 if check_repeat2(string) and check_repeat3(string) else 0

print("Part 2:", count)
