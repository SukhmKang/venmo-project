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
        return False
    cursor.execute(''' SELECT username FROM users WHERE username =?''', (recipientID,))
    if cursor.fetchone() == None:
        print("Error: Recipient not in system.")
        return False
    if not verifiedtime(senderID,120,cursor):
        print(f"Error: To complete a payment you must verify your account in the past 120 days.")
        return False

    #error checking: need to check if amount is a numerical value or not
    try:
        amount = float(amount)
        if amount <= 0:
            print("Error: You cannot pay someone 0 or negative dollars.")
            return False
    except ValueError:
        print("Error: Did not input a numerical payment amount.")
        return False

    #checks if you are friends
    if not friendchecker(senderID,recipientID,cursor):
        return False

    cursor.execute(''' SELECT privacy FROM users WHERE username=? ''', (senderID,))
    senderprivacy = ''.join(cursor.fetchone())
    cursor.execute(''' SELECT privacy FROM users WHERE username=? ''', (recipientID,))
    recipientprivacy = ''.join(cursor.fetchone())

    if privacy == None: 
        if senderprivacy == "Private" or recipientprivacy == "Private":
            privacy = "Private"
        elif senderprivacy == "Friends Only" or recipientprivacy == "Friends Only":
            privacy = "Friends Only"
        elif senderprivacy == "Public" or recipientprivacy == "Public":
            privacy = "Public"
        else:
            print("Error: Neither user has a default privacy setting and a privacy setting was not manually inputted.")
            return False
            
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
    else:
            print("======\nError: Invalid privacy setting.\nNote: Privacy options include:\nPrivate\nFriends Only\nPublic\n======")
            return False

    if tag != None and tag.lower().strip() not in tags:
        print(f"Error: Invalid tag. Valid tags are:\n {tags}")
        return False
    
    senderBalance = getbalance(senderID, cursor)
    recipientBalance = getbalance(recipientID, cursor)

    if amount > senderBalance:
        print("Error: Sender does not have enough money in account.")
        return False

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
    return True

def bankcheck(bankID):
    check = len(bankID) == 9 and bankID.isnumeric()
    if not check:
        print("Error: Bank routing number is not valid.\nNote: Routing numbers must contain exactly 9 numerical digits.")
    return check

def privacycheck(privacy):
    check = (privacy.lower() == "private") or (privacy.lower() == "friends only") or (privacy.lower() == "public")
    if not check:
        print("======\nError: Invalid privacy setting.\nNote: Privacy options include:\nPrivate\nFriends Only\nPublic\n======")
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
    
    print(f"Bank {bankID} successfully linked!")

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

def acceptrequest(senderID,paymentID,cursor,privacy=None):
    #making sure sender is in the system
    if not validateuser(senderID,cursor):
        return
    #making sure the user has active incoming requests
    hasactiverequests = False
    cursor.execute(''' SELECT paymentID FROM paymentLog WHERE status=? AND senderID=?''',("request",senderID))
    if cursor.fetchone():
        hasactiverequests = True

    cursor.execute(''' SELECT status FROM paymentLog WHERE paymentID=? AND senderID=?''',(paymentID,senderID))
    try:
        request_status = fetch(cursor.fetchone())
        if request_status == "cancelled_request":
            print("Error: This request was already cancelled.")
            return
        elif request_status =="denied_request":
            print("Error: You already denied this request.")
            return
        elif request_status =="accepted_request":
            print("Error: You already accepted this request.")
            return
        elif request_status =="_payment":
            print("Error: This payment ID corresponds to a payment, not a request.")
            return
        elif request_status == "*payment":
            print("Error: This payment ID corresponds to a transfer, not a request.")
            return
    except TypeError:
        if hasactiverequests:
            print("Error: Request ID is incorrect.")
            return
        print("Error: User has no requests.")
        return

    #storing the person who sent the request as recipientID
    cursor.execute(''' SELECT recipientID FROM paymentLog WHERE paymentID=? AND senderID=?''',(paymentID,senderID))
    recipientID = fetch(cursor.fetchone())
    #making sure recipient still exists in the userbase
    cursor.execute(''' SELECT username FROM users WHERE username LIKE ? ''',(recipientID,))
    if cursor.fetchone() == None:
        print("Error: The user who requested you no longer exists.")
        return
    #making sure sender and recipient are still friends
    if not friendchecker(senderID,recipientID,cursor):
        print("Note: In order to accept a request, you must be friends with the recipient at time of acceptance.")
        return
    
    #get the amount and message from the request
    cursor.execute(''' SELECT amount FROM paymentLog WHERE paymentID=? AND senderID=?''',(paymentID,senderID))
    amount = float(str(cursor.fetchone()).replace("(","").replace(")","").replace(",",""))
    cursor.execute(''' SELECT message FROM paymentLog WHERE paymentID=? AND senderID=?''',(paymentID,senderID))
    message = fetch(cursor.fetchone())
    cursor.execute(''' SELECT tag FROM paymentLog WHERE paymentID=? AND senderID=?''',(paymentID,senderID))
    #gets the tag (if exists) and pays the recipient the requested amount and logs the transaction and updates the request log too
    try:
        tag = fetch(cursor.fetchone())
        if pay(senderID, recipientID, amount, message, cursor, tag, privacy):
            cursor.execute(''' UPDATE paymentLog SET status=? WHERE paymentID=? AND senderID=? ''',("accepted_request",paymentID,senderID))
    except TypeError:
        if pay(senderID, recipientID, amount, message, cursor, None, privacy):
            cursor.execute(''' UPDATE paymentLog SET status=? WHERE paymentID=? AND senderID=? ''',("accepted_request",paymentID,senderID))

def unrequest(recipientID,paymentID,cursor):
    #making sure user exists
    if not validateuser(recipientID,cursor):
        return
    #making sure the user has outgoing active requests
    hasactiverequests = False
    cursor.execute(''' SELECT paymentID FROM paymentLog WHERE status=? AND recipientID=?''',("request",recipientID))
    if cursor.fetchone():
        hasactiverequests = True
    
    #checking status of the specified request
    cursor.execute(''' SELECT status FROM paymentLog WHERE paymentID=? AND recipientID=?''',(paymentID,recipientID))
    try:
        request_status = fetch(cursor.fetchone())
        if request_status == "request":
            cursor.execute(''' UPDATE paymentLog SET status =? WHERE paymentID=? AND recipientID=?''',("cancelled_request",paymentID,recipientID))
            print("Request successfully cancelled.")
        elif request_status == "cancelled_request":
            print("Error: User already cancelled this request.")
        elif request_status == "denied_request":
            print("Error: This request was already denied.")
        elif request_status == "accepted_request":
            print("Error: This request was already accepted.")
        elif request_status =="_payment":
            print("Error: This payment ID corresponds to a payment, not a request.")
            return
        elif request_status == "*payment":
            print("Error: This payment ID corresponds to a transfer, not a request.")
            return

    except TypeError:
        if hasactiverequests:
            print("Error: Payment ID is incorrect.")
            return
        print("Error: User has no active outgoing requests.")

def denyrequest(senderID,paymentID,cursor):
    if not validateuser(senderID,cursor):
        return
    #making sure the sender has incoming requests in his/her name
    hasactiverequests = False
    cursor.execute(''' SELECT paymentID FROM paymentLog WHERE status=? AND senderID=?''',("request",senderID))
    if cursor.fetchone():
        hasactiverequests = True

    cursor.execute(''' SELECT status FROM paymentLog WHERE paymentID=? AND senderID=?''',(paymentID,senderID))
    try:
        request_status = fetch(cursor.fetchone())
        if request_status == "request":
            cursor.execute(''' UPDATE paymentLog SET status =? WHERE paymentID=? AND senderID=?''',("denied_request",paymentID,senderID))
            print("Request denied for request ID {paymentID}.")
        elif request_status == "cancelled_request":
            print("Error: This request was already cancelled.")
        elif request_status =="denied_request":
            print("Error: You already denied this request.")
        elif request_status =="accepted_request":
            print("Error: You already accepted this request.")
        elif request_status =="_payment":
            print("Error: This payment ID corresponds to a payment, not a request.")
            return
        elif request_status == "*payment":
            print("Error: This payment ID corresponds to a transfer, not a request.")
            return
    except TypeError:
        if hasactiverequests:
            print("Error: Payment ID is incorrect.")
            return
        print("Error: User has no requests.")

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

def balance(userID, password, cursor):
    if not validateuser(userID,cursor):
        return
    if not passwordchecker(userID,password,cursor):
        return
    print(f"Your balance is: ${getbalance(userID,cursor)}.")

def transfer(userID, amount, cursor, type="no fee"):
    if not validateuser(userID,cursor):
        print("Verification failed.")
        return
    if not verifiedtime(userID,90,cursor):
        print(f"Error: To transfer you must verify your account in the past 90 days.")
        return
    cursor.execute(''' SELECT bank FROM users WHERE username=?''',(userID,))
    userBank = fetch(cursor.fetchone())
    if userBank == "*":
        print("Error: User must set up bank account before transferring.")
        return
    #error checking: need to check if amount is a numerical value or not
    try:
        amount = float(amount)
        if amount <= 0:
            print("Error: You cannot pay someone 0 or negative dollars.")
            return False
    except ValueError:
        print("Error: Did not input a numerical payment amount.")
        return False
    #fee calculation step
    if type.lower() == "instant":
        fee = round(min((0.015 * amount),15),2)
        type = "Instant Transfer"
    elif type.lower()=="no fee":
        fee = 0
        type = "No Fee Transfer"
    else:
        print("Error: Please enter a valid transfer type:\nTransfer types include:\n•Instant\n•No Fee")
        return
    
    userBalance = getbalance(userID,cursor)
    userBalance = userBalance - amount
    if userBalance < 0:
        print(f"You cannot transfer more than you have in your account. Current balance: {userBalance + amount}.")
        return
    #Updating users and paymentLog
    cursor.execute(''' UPDATE users SET balance=? WHERE username=?''',(userBalance,userID))
    cursor.execute(''' UPDATE users SET fees=fees+? WHERE username=?''',(fee,userID))
    cursor.execute(''' ''')
    
    #generating transfer ID
    transferID = hash(str(userID)+str(userBank)+str(type)+str(datetime.now()))
    print(f"${amount} transferred to Bank: {userBank}. Your new balance is ${userBalance}.")
    if fee > 0:
        print(f"Your fee for this transfer was: ${fee}")

    cursor.execute(''' INSERT INTO paymentLog (senderID, recipientID, amount, status, date, message, paymentID, privacy, tag, senderBalance, recipientBalance)
    VALUES (?,?,?,?,?,?,?,?,?,?,?) ''',(userID,userBank,amount,"transfer",datetime.now(),type,transferID,None,None,None,None))


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
    print(f"{userID} added {friendID} as a friend!")
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

def setprivacy(userID, privacy, cursor):
    if not validateuser(userID,cursor):
        return

    cursor.execute(''' SELECT privacy FROM users WHERE username=?''', (userID,))
    currPrivacy = fetch(cursor.fetchone())

    if privacy.lower() == "private":
        privacy = "Private"
    if privacy.lower() == "public":
        privacy = "Public"
    if privacy.lower() == "friends only":
        privacy = "Friends Only"

    if not privacycheck(privacy):
        return

    if privacy == currPrivacy:
        print(f"Error: Your privacy settings are already {privacy} ")
        return

    if currPrivacy != "*":
        print(f"Warning: This action will override your current setting: {currPrivacy}. To proceed, use updatePrivacy.\nUsage: updatePrivacy userID password privacy")
        return
    
    cursor.execute( ''' UPDATE users SET privacy=? WHERE username=?''',(privacy,userID))
    

def updateprivacy(userID, password, privacy, cursor):
    if not validateuser(userID,cursor):
        return
    
    if not passwordchecker(userID,password,cursor):
        return
    
    cursor.execute( ''' SELECT privacy FROM users WHERE username=?''',(userID,))
    oldPrivacy = fetch(cursor.fetchone())

    if privacy.lower() == "private":
        privacy = "Private"
    if privacy.lower() == "public":
        privacy = "Public"
    if privacy.lower() == "friends only":
        privacy = "Friends Only"

    if not privacycheck(privacy):
        return

    if privacy == oldPrivacy:
        print(f"Error: Attempting to override with the same privacy setting: {oldPrivacy}.")
        return

    cursor.execute( ''' UPDATE users SET privacy=? WHERE username=?''',(privacy,userID))
    print(f"Success! Your privacy settings have been changed to: {privacy}.")

def adduser(userID, password, accountType,cursor):
    if str(accountType.lower()) != "personal" and str(accountType.lower()) != "business":
        print("Error: Invalid account type.")
        return
    if accountType.lower() == "personal":
        accountType = "Personal"
    else:
        accountType = "Business"
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

def validatepayment(paymentID,cursor):
    cursor.execute(''' SELECT paymentID FROM paymentLog WHERE paymentID=?''',(paymentID,))
    if cursor.fetchone():
        return True
    else:
        print("Error: A payment with this ID does not exist.")
        return False

def transactionprivacy(userID,paymentID,newprivacy,cursor):
    if not validateuser(userID,cursor):
        return
    if not validatepayment(paymentID,cursor):
        return
    cursor.execute(''' SELECT senderID FROM paymentLog WHERE paymentID =? ''',(paymentID,))
    sender = fetch(cursor.fetchone())
    cursor.execute(''' SELECT recipientID FROM paymentLog WHERE paymentID =? ''',(paymentID,))
    recipient = fetch(cursor.fetchone())
    if userID != sender and userID != recipient:
        print(f"Error: {userID} was not involved in this payment.")
        return
    cursor.execute(''' SELECT privacy FROM paymentLog WHERE paymentID=?''',(paymentID,))
    privacy = fetch(cursor.fetchone())
    if newprivacy.lower() == "private":
        newprivacy = "Private"
    if newprivacy.lower() == "public":
        newprivacy = "Public"
    if newprivacy.lower() == "friends only":
        newprivacy = "Friends Only"
    if not privacycheck(newprivacy):
        return
    if newprivacy == privacy:
        print(f"Error: Payment privacy is already {privacy}.")
        return
    if (privacy == "Private") or (privacy == "Friends Only" and newprivacy == "Public"):
        print(f"Error: Since Transaction {paymentID} is {privacy}, it cannot be changed to {newprivacy}.")
        return
    if (privacy == "Friends Only" and newprivacy == "Private") or (privacy == "Public"):
        cursor.execute(''' UPDATE paymentLog SET privacy=? WHERE paymentID=?''',(newprivacy,paymentID))
        print(f"Privacy for Payment {paymentID} converted from {privacy} to {newprivacy}.")
    
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
