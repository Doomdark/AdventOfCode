from hashlib import md5

door_id = 'abbhdwsy'
#door_id = 'abc'

def get_password(door_id):

    password = ''
    index = 0

    while(1):
        string = door_id + str(index)

        # Hash it!
        md5hash = str(md5(string.encode('utf-8')).hexdigest())

        # Are the first 5 characters 0?
        if md5hash.startswith('00000'):
            password += md5hash[5]

        # If the password length is 8 then we're done
        if len(password) == 8:
            return password

        index += 1

#print("Part 1:", get_password(door_id))

def get_password2(door_id):

    password = [''] * 8
    index = 0

    while(1):
        string = door_id + str(index)

        # Hash it!
        md5hash = str(md5(string.encode('utf-8')).hexdigest())

        # Are the first 5 characters 0?
        if md5hash.startswith('00000'):
            try:
                posn = int(md5hash[5])
                char = md5hash[6]
                if password[posn] == '':
                    password[posn] = char
            except:
                pass

        # If the password length is 8 then we're done
        if not any([x == '' for x in password]):
            return ''.join(password)

        index += 1

print("Part 2:", get_password2(door_id))
