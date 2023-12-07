import sys

base = [0, 1, 0, -1]

input_signal = "12345678"
input_signal = "59719811742386712072322509550573967421647565332667367184388997335292349852954113343804787102604664096288440135472284308373326245877593956199225516071210882728614292871131765110416999817460140955856338830118060988497097324334962543389288979535054141495171461720836525090700092901849537843081841755954360811618153200442803197286399570023355821961989595705705045742262477597293974158696594795118783767300148414702347570064139665680516053143032825288231685962359393267461932384683218413483205671636464298057303588424278653449749781937014234119757220011471950196190313903906218080178644004164122665292870495547666700781057929319060171363468213087408071790"

def splitter(s):
    return [int(s[i]) for i in range(len(s))]

def make_multiplier(i, s, first):
    o = []
    required_length = len(s) + (1 if first else 0)
    while len(o) < required_length:
        for b in base:
            for j in range(i):
                o.append(b)
    return o

def multiply(s, first):
    o = []

    for i in range(len(s)):
        m = make_multiplier(i+1, s, first)
        # Ignore the first multiplier entry for the very first loop
        m = m[1:]
        # Truncate the array to the length of s
        m = m[:len(s)]
        # Multiply the input signal array with the multiplier array
        n = [x*s[j] for j,x in enumerate(m)]
        # Now sum the products
        q = abs(sum(n)) % 10
        #print i, m, n, q
        # Append the result to the array
        o.append(q)

    return o

first = True
phase = 1

signal = splitter(input_signal)
print phase, signal[:8]

while True:
    signal = multiply(signal, first)

    print phase, ''.join([str(x) for x in signal[:8]])

    first = False

    if phase == 100:
        break

    phase += 1
