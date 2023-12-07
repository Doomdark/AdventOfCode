import re

passmatch = re.compile('(\w+):(\S+)')

valids = []
passport = {}

def is_valid(p):
    if 'byr' in p and 'iyr' in p and 'eyr' in p and 'hgt' in p and 'hcl' in p and 'ecl' in p and 'pid' in p:
        return True
    else:
        return False
    
with open("Day04_input.txt") as f:
    for line in f.readlines():
        match = passmatch.findall(line)
        if match:
            for cat, val in match:
                passport[cat] = val
        else:
            # Process passport now
            if is_valid(passport):
                valids.append(passport)
            passport = {}

print ("Part 1:", len(valids))

byrmatch = re.compile('(\d\d\d\d)')
iyrmatch = re.compile('(\d\d\d\d)')
eyrmatch = re.compile('(\d\d\d\d)')
hgtmatch = re.compile('(\d+)(\w+)')
hclmatch = re.compile('(#[a-f0-9]{6})')
eclmatch = re.compile('(amb|blu|brn|gry|grn|hzl|oth)')
pidmatch = re.compile('(\d{9}(?:\d{2})?$)')

valids = []

with open("Day04_input.txt") as f:
    for line in f.readlines():
        match = passmatch.findall(line)
        if match:
            #print match
            for cat, val in match:
                # Check validity of fields
                if cat == 'byr':
                    match = byrmatch.match(val)
                    if match:
                        if int(val) >= 1920 and int(val) <= 2002:
                            passport[cat] = val
                if cat == 'iyr':
                    match = iyrmatch.match(val)
                    if match:
                        if int(val) >= 2010 and int(val) <= 2020:
                            passport[cat] = val
                if cat == 'eyr':
                    match = eyrmatch.match(val)
                    if match:
                        if int(val) >= 2020 and int(val) <= 2030:
                            passport[cat] = val
                if cat == 'hgt':
                    match = hgtmatch.match(val)
                    if match:
                        hgt = int(match.group(1))
                        unit = match.group(2)
                        if unit == "cm":
                            if hgt >= 150 and hgt <= 193:
                                passport[cat] = val
                        if unit == "in":
                            if hgt >= 59 and hgt <= 76:
                                passport[cat] = val
                if cat == 'hcl':
                    match = hclmatch.match(val)
                    if match:
                        passport[cat] = val
                if cat == 'ecl':
                    match = eclmatch.match(val)
                    if match:
                        passport[cat] = val
                if cat == 'pid':
                    match = pidmatch.match(val)
                    if match:
                        passport[cat] = val
        else:
            # Process passport now
            #print "Passport:", passport
            if is_valid(passport):
                valids.append(passport)
                #print ({k:v for k,v in sorted(passport.items(), key=lambda item: item[0])})
            passport = {}

print ("Part 2:", len(valids))

