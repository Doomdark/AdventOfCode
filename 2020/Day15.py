starting = [0,3,6]
starting = [2,20,0,4,1,17]
numbers = {}
count = 0
last = None
while count <30000000:
    if count < len(starting):
        s = set()
        s.add(count)
        numbers[starting[count]] = s
        last = starting[count]
    else:
        # Now look at the last number. If it has only been said once then update 0.
        #print("Last:",last)
        
        _s = numbers[last]

        # Choose the number to speak. If this number has only been said once then say 0.
        if len(_s) == 1:
            _n = 0
        else: # Otherwise it's the difference between the 2 numbers to say
            _n = max(_s) - min(_s)
        # print("Say:",_n)
        
        # Get the set of the number being said
        if _n not in numbers:
            s = set()
            s.add(count)
            numbers[_n] = s
            last = _n
        else:
            # Get the number set
            _s = numbers[_n]
            # Add the current count
            _s.add(count)
            #print(_s)
            # If there are more than 2 in the set then remove the oldest
            if len(_s) > 2:
                _s.remove(min(_s))
            # Update the number again
            numbers[_n] = _s
                
        # Update last
        last = _n
        
    #print(last)
    count += 1
print("Part 1:",last)
