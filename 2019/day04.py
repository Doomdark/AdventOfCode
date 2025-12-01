valid = []

for i in range(357253, 892942+1):
    s = str(i)

    doubles    = {}
    largers    = {}
    increasing = True

    for c in range(len(s)-1):
        if s[c+1] < s[c]:
            increasing = False
            break
        # Check for matching the last digit
        if s[c+1] == s[c]:
            # Already got a double of this one?
            if s[c] not in largers:
                if s[c] in doubles:
                    largers[s[c]] = 1
                    del doubles[s[c]]
                else:
                    doubles[s[c]] = 1

    if increasing and doubles:
        valid.append(i)

print("Part 2:", len(valid))
