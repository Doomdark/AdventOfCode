import re

cat_match = re.compile(r'([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)')

mine = []
others = []
categories = {}
cats = True
m = False

with open("Day16_input.txt") as f:
    for line in f.readlines():
        if cats:
            match = cat_match.match(line.rstrip())
            if match:
                s = set()
                for i in range(int(match.group(2)), int(match.group(3))+1):
                    s.add(i)
                for i in range(int(match.group(4)), int(match.group(5))+1):
                    s.add(i)
                categories[match.group(1)] = s
            else:
                cats = False
                m = True
        elif m:
            if ',' in line:
                mine = [int(x) for x in line.rstrip().split(',')]
                m = False
        else: # Others
            if ',' in line:
                o = [int(x) for x in line.rstrip().split(',')]
                others.append(o)

invalids = []
valids = []

for ticket in others:
    valid = True
    for v in ticket:
        # Is this value in any of the ranges in the dictionary categories?
        if not any(v in s for c,s in categories.items()):
            invalids.append(v)
            valid = False
    if valid:
        valids.append(ticket)

print ("Part 1:", sum(invalids))

possible = {}

# Get the field orders. Do each column in turn as each ticket is in the same order.
for col in range(len(valids[0])):
    possibilities = set()
    # Get all the fields for this column number
    fields = [valids[i][col] for i in range(len(valids))]
    # Check each rule to see if all of the field values appear in the value set
    for rule, s in categories.items():
        # Check if all the column values appear in the rule. All the values must appear in the rule set for this rule to be a possibility.
        if all(field in s for field in fields):
            possibilities.add(rule)
    # The possible rules for this column
    possible[col] = possibilities

# Now we've got a set of possible rules for each column in the ticket.

# Make a set to hold the rules found already
rules_identified = set()
# Make a dictionary to hold the column assigned for each found rule
confirmed_fields = {}

# Iterate until the confirmed field list length is the same length as the possible column dictionary
while len(confirmed_fields.keys()) < len(possible.keys()):
    # Check every possible column each time
    for col, rules in possible.items():
        # If the rules minus the rules identified == 1 then this column definitely matches that rule
        if len(rules - rules_identified) == 1:
            # Get the rule now that it matches
            rule = min(rules - rules_identified)
            # Assign the column number to the rule
            confirmed_fields[rule] = col
            # Add the rule to the found set
            rules_identified.add(rule)

# Get the six rule positions whose names begin with "departure"
import math

print("Part 2:", math.prod([mine[c] for n,c in confirmed_fields.items() if n.startswith("departure")]))
      
