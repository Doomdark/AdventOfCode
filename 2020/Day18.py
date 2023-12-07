sums = []

with open("Day18_input.txt") as f:
    for line in f.readlines():
        if not line.startswith('#'):
            sums.append(line.rstrip())

# Make some matchers for finding stuff in the strings
import re
match_num     = re.compile('^(\d+)')
findall_exprs = re.compile('([\+\*\-]\s*\d+)+')
findall_adds  = re.compile('(\d+ \+ \d+)')

def add_parens(expr):
    '''Add parentheses around standalone additions'''
    _expr = expr
    adds = findall_adds.findall(expr)
    for add in adds:
        _expr = _expr.replace(add,'('+add+')',1)
    return _expr

def evaluate(expr,part2=False):
    '''Evaluate the provided expression'''
    _expr = ''
    posn = 0
    # Traverse the provided expression
    while posn < len(expr):
        # Append the current character to the new string if it's not an open parenthesis
        if expr[posn] != '(':
            # Append the character to the current expression
            _expr += expr[posn]
            # Move on by one character
            posn += 1
        else: # Otherwise search for the matching parenthesis
            # Start looking at the next character
            _posn = posn + 1
            # Levels of parentheses
            level = 0
            # Search the rest of the string for a close parenthesis
            while _posn < len(expr):
                # Found a close parenthesis
                if expr[_posn] == ')':
                    # Is it a level 0 parenthesis?
                    if level == 0:
                        _end = _posn
                        break
                    else: # Nope - go down a level
                        level -= 1
                # Found another open parenthesis. Go up a level.
                elif expr[_posn] == '(':
                    level += 1
                # Next character
                _posn += 1
            # Got a parenthesis match now so call evaluate on the sub-string
            _expr += evaluate(expr[posn+1:_posn],part2) # Remove parentheses
            # Move the position on to the next character and keep traversing
            posn += (_posn-posn+1)

    # Now we've got to a parenthesis-less expression, look for additions and put parentheses around them
    # then re-evaluate the expression again to do those first.
    if part2:
        # If there are any additions (plus any other operators) left then add praentheses and re-evaluate.
        # If there are additions and no other operators then don't add parentheses.
        while '+' in _expr and (expr.count('*') > 0 or expr.count('-') > 0):
            _expr = add_parens(_expr)
            _expr = evaluate(_expr,True)
        
    # Evaluation becomes a regexp with in-order eval

    # Get the initial value
    val = match_num.match(_expr).group(1)
    # Find all the subsequent operators
    exprs = findall_exprs.findall(_expr)
    # Eval each operator in turn with the current total
    for e in exprs:
        _e = val+e
        val = str(eval(_e))
    return str(val)

part1 = 0

for sum in sums:
    part1 += int(evaluate(sum))

print("Part 1:", part1)


part2 = 0

for sum in sums:
    part2 += int(evaluate(sum,True))

print("Part 2:", part2)
