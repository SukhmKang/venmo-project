from datetime import datetime
tags = ["food", "groceries", "rent", "utilities", "sports", "fun", "transportation", "drinks", "business", "tickets", "gift", "gas"]
cmds = ["pay","linkbank","override","request","transfer","deposit"]

def fetch(fetchone):
    return str(''.join(fetchone))

def isverified(userID,cursor):
    cursor.execute(''' SELECT ssn FROM users WHERE username=?''',(userID,))
    ssn = fetch(cursor.fetchone())
    if ssn == "*":
        print("Error: User is not verified.")
        return False
    return True

#Checks if user inputs correct password
def passwordchecker(userID,password,cursor):
    cursor.execute( ''' SELECT password FROM users WHERE username=?''',(userID,))
    correctpassword = str(''.join(cursor.fetchone()))
    if password != correctpassword:
        print("Error: Incorrect password.")
        return False
    return True

#Accesses current user balance
def getbalance(userID,cursor):
    cursor.execute(''' SELECT balance FROM users WHERE username=? ''', (userID,))
    userBalance = str(cursor.fetchone()).replace("(","").replace(")","").replace(",","")
    userBalance = float(userBalance)
    return userBalance

#checks if a user currently exists
def validateuser(userID,cursor):
    cursor.execute(''' SELECT username FROM users WHERE username=?''', (userID,))
    if cursor.fetchone() == None:
        print("Error: User not in system.")
        return False
    return True

#checks if user has verified account in given time period
def verifiedtime(userID,days,cursor):
    if not validateuser(userID,cursor):
        return
    cursor.execute( ''' SELECT verification FROM users WHERE username=?''',(userID,))
    lastVerified = ''.join(cursor.fetchone())
    lastVerified = datetime.strptime(lastVerified, '%Y-%m-%d %H:%M:%S.%f')
    difference = str((datetime.now() - lastVerified))
    if "days" not in difference:
        return True
    daydifference = ""
    for character in difference:
        if character == " ":
            break
        daydifference += character
    return int(daydifference) < days

#Checks if user has friended another user and/or if the other user has friended them back
def friendchecker(senderID,recipientID,cursor):
    cursor.execute(''' SELECT friends FROM users WHERE username=?''',(senderID,))
    senderFriends = ''.join(cursor.fetchone())
    if recipientID not in senderFriends:
        print("Error: You are not friends with " + recipientID + ".")
        return False
    cursor.execute(''' SELECT friends FROM users WHERE username=?''',(recipientID,))
    recipientFriends = ''.join(cursor.fetchone())
    if senderID not in recipientFriends:
        print("Error: " + recipientID + " has not friended you back.")
        return False
    return True

#Sends payment from one user to another
def pay(senderID,recipientID,amount,message,cursor,tag=None,privacy=None):
    cursor.execute(''' SELECT username FROM users WHERE username=?''', (senderID,))
    if cursor.fetchone() == None:
        print("Error: Sender not in system.")
        return
    cursor.execute(''' SELECT username FROM users WHERE username =?''', (recipientID,))
    if cursor.fetchone() == None:
        print("Error: Recipient not in system.")
        return
    if not verifiedtime(senderID,120,cursor):
        print(f"Error: To complete a payment you must verify your account in the past 120 days.")
        return

    #error checking: need to check if amount is a numerical value or not
    try:
        amount = float(amount)
        if amount <= 0:
            print("Error: You cannot pay someone 0 or negative dollars.")
            return
    except ValueError:
        print("Error: Did not input a numerical payment amount.")
        return

    #checks if you are friends
    if not friendchecker(senderID,recipientID,cursor):
        return

    cursor.execute(''' SELECT privacy FROM users WHERE username=? ''', (senderID,))
    senderprivacy = ''.join(cursor.fetchone())
    cursor.execute(''' SELECT privacy FROM users WHERE username=? ''', (recipientID,))
    recipientprivacy = ''.join(cursor.fetchone())

    if privacy == None: 
        if senderprivacy or recipientprivacy == "Private":
            privacy = "Private"
        elif senderprivacy or recipientprivacy == "Friends Only":
            privacy = "Friends Only"
        elif senderprivacy == "Public" and recipientprivacy == "Public":
            privacy = "Public"
        else:
            print("Error: Neither user has a default privacy setting and a privacy setting was not manually inputted.")
            return
    elif privacy.lower() == "private":
        privacy = "Private"
    elif privacy.lower() == "friends only":
        if recipientprivacy == "Private":
            privacy = "Private"
        else:
            privacy = "Friends Only"
    elif privacy.lower() == "public":
        if recipientprivacy == "Private":
            privacy = "Private"
        elif recipientprivacy == "Friends Only":    
            privacy = "Friends Only"
        else:
            privacy = "Public"

    if privacy.lower() != "private" and privacy.lower() != "friends Only" and privacy.lower() != "public":
        print("Error: Privacy input must be 'Privacy' or 'Friends Only' or 'Public'.")
        return

    if tag != None and tag.lower().strip() not in tags:
        print(f"Error: Invalid tag. Valid tags are:\n {tags}")
        return
    
    senderBalance = getbalance(senderID, cursor)
    recipientBalance = getbalance(recipientID, cursor)

    if amount > senderBalance:
        print("Error: Sender does not have enough money in account.")
        return

    # hashing function to generate payment ID
    paymentID = hash(str(senderID)+str(recipientID)+str(message)+str(datetime.now()))

    #updating user balance
    senderBalance = senderBalance - amount
    recipientBalance = recipientBalance + amount
    cursor.execute(''' UPDATE users SET balance = ? WHERE username=? ''',(senderBalance,senderID))
    cursor.execute(''' UPDATE users SET balance = ? WHERE username=? ''',(recipientBalance,recipientID))
    cursor.execute(''' INSERT INTO paymentLog (senderID, recipientID, amount, status, date, message, paymentID, privacy, tag, senderBalance, recipientBalance)
    VALUES (?,?,?,?,?,?,?,?,?,?,?) ''',(senderID,recipientID,amount,"_payment",datetime.now(),message,paymentID,privacy,tag,senderBalance,recipientBalance))
    print(f"Successfuly paid {recipientID} ${amount}")

def bankcheck(bankID):
    check = len(bankID) == 9 and bankID.isnumeric()
    if not check:
        print("Error: Bank routing number is not valid.\nNote: Routing numbers must contain exactly 9 numerical digits.")
    return check

def ssncheck(SSN):
    SSN = SSN.replace("-","").replace(" ","")
    check = len(SSN) == 9 and SSN.isnumeric()
    if not check:
        print("Error: SSN is not valid.\nNote: SSN must contain exactly 9 numerical digits. Dashes and spaces are okay.")
    return check

def linkbank(userID, bankID, cursor):
    if not validateuser(userID,cursor):
        return
    
    if not isverified(userID,cursor):
        print("You must verify your account before linking a bank account.")
        return

    if not verifiedtime(userID,60,cursor):
        print(f"Error: To link your bank you must verify your account in the past 60 days.")
        return

    cursor.execute(''' SELECT bank FROM users WHERE username=?''', (userID,))
    bankcode = str(''.join(cursor.fetchone()))

    #checks if person already has the same bank account
    if bankID == bankcode:
        print("Error: You have already linked this bank account.")
        return

    if bankcode != "*":
        print(f"Warning: This action will override your current bank: {bankcode}. To proceed, use override.\nUsage: override userID password bankID")
        return

    if bankcheck(bankID):
        cursor.execute( ''' UPDATE users SET bank=? WHERE username=?''',(bankID,userID))

def override(userID, password, bankID, cursor):
    if not validateuser(userID,cursor):
        return
    if not passwordchecker(userID,password,cursor):
        return
    
    if not verifiedtime(userID,60,cursor):
        print(f"Error: To override your bank you must verify your account in the past 60 days.")
        return

    cursor.execute( ''' SELECT bank FROM users WHERE username=?''',(userID,))
    oldbank = str(''.join(cursor.fetchone()))
    if bankID == oldbank:
        print("Error: Attempting to override with the same ID.")
    if bankcheck(bankID):
        cursor.execute( ''' UPDATE users SET bank=? WHERE username=?''',(bankID,userID))

def request(userID, friendID,amount,message,cursor,tag=None):
    #checks if user exists
    if not validateuser(userID,cursor):
        return
    
    #checks if friendID exists
    cursor.execute(''' SELECT username FROM users WHERE username=?''', (friendID,))
    if cursor.fetchone() == None:
        print("Error: No account exists with " + friendID + " as its username.")
        return

    #checks if user has verified in the past 120 days
    if not verifiedtime(userID,120,cursor):
        print(f"Error: To request you must verify your account in the past 120 days.")
        return
    
    #checks if amount is a number
    try:
        amount = float(amount)
        if amount <= 0:
            print("Error: You cannot request 0 or negative dollars.")
            return
    except ValueError:
        print("Error: Did not input a numerical payment amount.")
        return

    #checks if you are friends with friendID
    if not friendchecker(userID,friendID,cursor):
        return

    #generates requestID
    requestID = hash(str(userID)+str(friendID)+str(message)+str(datetime.now()))

    cursor.execute(''' INSERT INTO paymentLog (senderID, recipientID, amount, status, date, message, paymentID, privacy, tag, senderBalance, recipientBalance)
    VALUES (?,?,?,?,?,?,?,?,?,?,?) ''',(friendID,userID,amount,"request",datetime.now(),message,requestID,None,tag,None,None))

    return

def unrequest(paymentID):
    return

def deposit(userID, amount, cursor):
    if not validateuser(userID,cursor):
        return
    
    if not verifiedtime(userID,90,cursor):
        print(f"Error: To deposit you must verify your account in the past 90 days.")
        return
    
    try:
        amount = float(amount)
        if amount <= 0:
            print("Error: You cannot deposit a negative amount of money into your Venmo.")
            return
    except ValueError:
        print("Error: Did not input a numerical amount.")
        return
    cursor.execute( ''' SELECT bank FROM users WHERE username=?''',(userID,))
    bankID = str(''.join(cursor.fetchone()))
    if bankID == "*":
        print("Error: You do not have bank account set up.\nUse linkBank to add your information.")
        return
    userBalance = getbalance(userID,cursor)
    userBalance += amount
    cursor.execute( ''' UPDATE users SET balance=? WHERE username =?''',(userBalance,userID))
    return

def verify(userID,password,SSN,cursor):
    if not validateuser(userID,cursor):
        print("Verification failed.")
        return
    if not passwordchecker(userID,password,cursor):
        print("Verification failed.")
        return
    #make sure the user inputted a valid SSN
    if not ssncheck(SSN):
        print("Verification failed.")
        return
    SSN = SSN.replace("-","").replace(" ","")
    cursor.execute(''' SELECT ssn FROM users WHERE username=?''',(userID,))
    verifiedSSN = str(''.join(cursor.fetchone()))
    if verifiedSSN == "*":
        cursor.execute(''' UPDATE users SET ssn=? WHERE username=?''',(str(SSN),userID))
        cursor.execute(''' UPDATE users SET verification=? WHERE username=?''',(datetime.now(),userID))
        print("Your account has successfully been verified!")
        return
    if SSN == verifiedSSN:
        cursor.execute(''' UPDATE users SET verification=? WHERE username=?''',(datetime.now(),userID))
        return
    else:
        print("Verification failed. SSN incorrect ")

def transfer(userID, amount, type, cursor):
    if not validateuser(userID,cursor):
        print("Verification failed.")
        return

    if not verifiedtime(userID,90,cursor):
        print(f"Error: To transfer you must verify your account in the past 90 days.")
        return

    return

def friend(userID, friendID, cursor):
    if not validateuser(userID,cursor):
        return

    cursor.execute(''' SELECT username FROM users WHERE username=?''', (friendID,))
    if cursor.fetchone() == None:
        print("Error: No account exists with " + friendID + " as its username.")
        return

    cursor.execute(''' SELECT friends FROM users WHERE username=?''', (userID,))
    currentFriends = ''.join(cursor.fetchone())
    if friendID in currentFriends:
        print("Error: You are already friends with " + friendID + ".")
        return
    
    cursor.execute(''' SELECT friends FROM users WHERE username=?''', (userID,))

    if currentFriends != "*":
        updatedFriends = str(currentFriends) + "," + friendID
    else:
        updatedFriends = friendID

    cursor.execute(''' UPDATE users SET friends = ? WHERE username=? ''',(updatedFriends, userID))
    return

def unfriend(userID, friendID, cursor):
    #common checks for user and friend
    if not validateuser(userID,cursor):
        return

    cursor.execute(''' SELECT username FROM users WHERE username=?''', (friendID,))
    if cursor.fetchone() == None:
        print("Error: No account exists with " + friendID + " as its username.")
        return

    cursor.execute(''' SELECT friends FROM users WHERE username=?''', (userID,))
    currentFriends = ''.join(cursor.fetchone())
    if friendID not in currentFriends:
        print("Error: You are not friends with " + friendID + ".")
        return

    #string manipulation of user's friends (removing the unfriended username from the friends string)
    indexSubstring = currentFriends.find(friendID)
    lenFriendID = len(friendID)
    updatedFriends = ""

    #friendID is user's only friend
    if len(currentFriends) == lenFriendID:
        updatedFriends = "*"
    #friendID is user's first (but not only) friend
    elif indexSubstring == 0:
        updatedFriends = currentFriends[lenFriendID + 1:]
    #friendID is user's most recent friend
    elif indexSubstring + lenFriendID == len(currentFriends):
        updatedFriends = currentFriends[0:len(currentFriends)-(lenFriendID + 1)]
    #friendID is neither the first or the latest friend (somewhere in the middle of the friends string)
    else:
        updatedFriends = currentFriends[0: indexSubstring] + currentFriends[indexSubstring + lenFriendID + 1:]
    
    #updating the friends string in the users database
    cursor.execute(''' UPDATE users SET friends = ? WHERE username=? ''',(updatedFriends, userID))

    #calling unfriend for friendID (this action is forced by userID's unfriend command) 
    cursor.execute(''' SELECT friends FROM users WHERE username=?''', (friendID,))
    friendsFriends = ''.join(cursor.fetchone())
    if userID in friendsFriends:
        unfriend(friendID, userID, cursor)

def checkpassword(password):
    checks = [False,False,False,False]
    errormessages = ["• 8 characters","• an uppercase letter","• a lowercase letter","• a number"]
    #length
    checks[0] = (len(password) >= 8)
    #uppercase
    #lowercase
    if not password.isnumeric():
        checks[1] = (not password.islower())
        checks[2] = (not password.isupper()) 
    #number
    for character in password:
        if character.isdigit():
            checks[3] = True
            break

    errormessage = "======\nPassword requirements: At least 8 characters length, including at least one uppercase letter, one lowercase letter, and one number.\nYour password does not have:\n"
    for i in range(len(checks)):
        if checks[i] == False:
            errormessage += errormessages[i] + "\n"
    if False in checks:
        print(f"{errormessage}======")
    return False not in checks

def setprivacy():
    return

def adduser(userID, password, accountType,cursor):
    if str(accountType.lower()) != "personal" and str(accountType.lower()) != "business":
        print("Error: Invalid account type.")
        return
    cursor.execute(''' SELECT username FROM users WHERE username LIKE ?''', (userID,))
    if cursor.fetchone():
        print("Error: Account with that username already exists.")
        return

    if not checkpassword(password):
        return

    cursor.execute(''' INSERT INTO users (username, friends, balance, accounttype, password) 
    VALUES (?,?,?,?,?) ''',
    (userID, "*", 0.0, accountType, password))
    return

def globallog(argv):
    return

def friendlog(argv):
    return

def personallog(argv):
    return

def transactionslog(argv):
    return

def requestlog(argv):
    return

def viewprofile(userID):
    return
