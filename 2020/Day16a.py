def check_rule(rule, fields):
    ''' checks whether each value in fields satisfies the specified rule '''
    first_criteria = range(rule[0][0], rule[0][1] + 1)
    second_criteria = range(rule[1][0], rule[1][1] + 1)
    return all([field in first_criteria or field in second_criteria for field in fields])

# extract input from file
with open('Day16_input.txt', 'r') as f:
    lines = [x.rstrip() for x in f.readlines()]

# convert rules to dict
rules = {}
for rule in lines[:20]:
    field_name = rule.split(': ')[0]
    first_criteria = rule.split(': ')[1].split(' or ')[0]
    range_one_min = int(first_criteria.split('-')[0])
    range_one_max = int(first_criteria.split('-')[1])
    second_criteria = rule.split(': ')[1].split(' or ')[1]
    range_two_min = int(second_criteria.split('-')[0])
    range_two_max = int(second_criteria.split('-')[1])
    rules[field_name] = [(range_one_min, range_one_max), (range_two_min, range_two_max)]

# discard invalid fields
min_range = min(criteria[0] for rule in rules.values() for criteria in rule)
max_range = max(criteria[1] for rule in rules.values() for criteria in rule)
valid = []
for line in lines[25:]:
    fields = [int(x) for x in line.split(',')]
    if all([field in range(min_range, max_range + 1) for field in fields]):
        valid.append(fields)

possible = {}
# for each column
for col in range(len(valid[0])):
    possible_rules = []
    # check rules that work for the entire column
    fields = [valid[i][col] for i in range(len(valid))]
    for rule, criteria in rules.items():
        if check_rule(criteria, fields):
            possible_rules.append(rule)
    possible[col] = possible_rules

# noticing that it is possible to sort the columns such that
# the number of rules in each column can differ by 1
ordered_pairs = sorted([(len(val), key) for key, val in possible.items()])
ordered_cols = [x[1] for x in ordered_pairs]

# determine which fields correspond to which column
confirmed_fields = {}
for col in ordered_cols:
    possible_rules = possible[col]
    # remove already confirmed rules from possible rules
    for field in confirmed_fields.keys():
        possible_rules.remove(field)
    confirmed_fields[possible_rules[0]] = col

print (confirmed_fields)

# find answer
ticket = [int(x) for x in lines[22].split(',')]
product = 1
for key, value in confirmed_fields.items():
    if key.startswith('departure'):
        product *= ticket[value]

print(product)
