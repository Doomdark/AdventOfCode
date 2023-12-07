rules = {}
messages = []

import re, itertools

rule_match = re.compile('^(\d+)\s*:\s+(.*)$')

with open("Day19_test2.txt") as f:
    _rules = True
    for line in f.readlines():
        match = rule_match.match(line)
        if match:
            num = int(match.group(1))
            rule = match.group(2).replace('"','')
            rules[num] = rule
        elif line.rstrip():
            messages.append(line.rstrip())

def resolve_subrules(rules,subrules,p=False):
    subrule_list = []

    # Get a list of rules being referenced by this subrule. This is a list of numbers.
    ref_rules_nums = [int(x) for x in subrules.split()]
    ref_rules      = [rules[n] for n in ref_rules_nums]

    # Only process if every entry in ref_rules has a or b in it
    process = True
    for ref_rule in ref_rules:
        # This rule is a list of other rules
        if isinstance(ref_rule,list):
            if not all([(('a' in x) or ('b' in x)) for x in ref_rule]):
                process = False
        elif ('a' not in ref_rule) and ('b' not in ref_rule):
            process = False

    if process:
        # Get all the combinations of the subrules
        print("Product before...")
        product_list = list(itertools.product(*ref_rules))
        print("Product after...", len(product_list))
        products = set()
        for i in product_list:
            p = ''.join(list(i))
            products.add(p)
        return list(products)
    else:
        return ''
    
import sys

def resolve_rules(rules):
    len_rules = len(rules)
    rules_done = set()
    count = 0
    
    # First set the rules done for those that don't need resolving
    for n,rule in rules.items():
        if 'a' in rule or 'b' in rule:
            rules_done.add(n)

    # Resolve all the rules
    while len(rules_done) < len_rules:
        # Iterate through all the rules
        for n, rule in rules.items():
            # We haven't processed it if the rule is not in the done set
            if n not in rules_done:
                rule_list = []
                add_rule = True
                # Split into subrules
                subrules = rule.split('|')
                # Iterate over those subrules
                for subrule in subrules:
                    subrule_return = resolve_subrules(rules,subrule.rstrip().lstrip())
                    if subrule_return != '':
                        rule_list.extend(subrule_return)
                    else:
                        add_rule = False
                # Add the rule
                if add_rule:
                    rules[n] = rule_list
                    rules_done.add(n)

    return rules

# Resolve all the rules into full strings
rules = resolve_rules(rules)

# How many messages match rule[0]? Make a set because set checking is super-fast.
rule_set = set(rules[0])

# Count the number of messages in the set
count = sum([m in rule_set for m in messages])

print ("Part 2:", count)

                           
