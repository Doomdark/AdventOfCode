ips = [ 'abba[mnop]qrst', 'abcd[bddb]xyyx', 'aaaa[qwer]tyui', 'ioxxoj[asdfgh]zxcvbn', 'qqqqqq[adfsf]fgqqsdgs' ]
ips = ['iniqqqqprdeznwhr[arooglolfjgprfrbhbm]sczcmpftuhbaagwgedq[yutgzaqyxntjxoglmb]vswbhlspwfulowkif']
ips = ['aba[bab]xyz', 'xyx[xyx]xyx', 'aaa[kek]eke', 'zazbz[bzb]cdb']

ips = []
with open("day07_input.txt") as f:
   for line in f.readlines():
       ips.append(line.strip())

def get_abba(f,s):
    return ''.join([f,s,s,f])

def check_for_abba(string):
    abbas = []

    first  = None
    second = None

    hypernet = False
    matches = []

    for i in range(len(string)-1):
        if string[i] == '[':
            first  = None
            second = None
            hypernet = True
        elif string[i] == ']':
            first  = None
            second = None
            hypernet = False
        elif first == None:
            first = string[i]
            #print("Assign first")
        elif second == None:
            #print("Assign second")
            second = string[i]
            # Identical abbas are not allowed
            if first == second:
                first = string[i]
                second = None
        else:
            #print("Check third")
            # Match abba
            #print(get_abba(first,second), string[i-2:i+2])
            if get_abba(first,second) == string[i-2:i+2]:
                matches.append((get_abba(first,second), hypernet))
                #print(get_abba(first,second))

            # Advance first and second
            first  = second
            second = string[i]

            if first == second:
                first = string[i]
                second = None

        #print(first, second)

    any_hypernet_matches = any([x[1] for x in matches])
    if any_hypernet_matches:
        return False
    else:
        if len(matches) > 0:
            #print(matches, any_hypernet_matches)
            return True

ip_count = 0
for ip in ips:
    #print('--', ip)
    if check_for_abba(ip):
        ip_count += 1
        #print(check_for_abba(ip), ip)

print("Part 1:", ip_count)


def get_aba(f,s):
    return ''.join([f,s,f])

def check_for_ssl(string):
    abas = []
    babs = []

    first  = None
    second = None

    hypernet = False

    for i in range(len(string)):
        if string[i] == '[':
            first  = None
            second = None
            hypernet = True
        elif string[i] == ']':
            first  = None
            second = None
            hypernet = False
        elif first == None:
            first = string[i]
        elif second == None:
            second = string[i]
            # Identical abbas are not allowed
            if first == second:
                first = string[i]
                second = None
        else:
            # Match aba
            if get_aba(first,second) == string[i-2:i+1]:
                #print("Match", hypernet)
                if hypernet:
                    babs.append((second,first))
                else:
                    abas.append((first,second))

            # Advance first and second
            first  = second
            second = string[i]

            if first == second:
                first = string[i]
                second = None

        #print(first,second)

    # Check each aba has a matching bab
    for aba in abas:
        aba_first, aba_second = aba
        for bab in babs:
            bab_first, bab_second = bab
            if bab_first == aba_first and bab_second == aba_second:
                return True

    return False

ip_count = 0
for ip in ips:
    #print('--', ip)
    if check_for_ssl(ip):
        ip_count += 1
        #print("Count:", ip_count)

print("Part 2:", ip_count)
