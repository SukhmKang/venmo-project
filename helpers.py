from datetime import datetime, timedelta
import re
tags = ["food", "groceries", "rent", "utilities", "sports", "fun", "transportation", "drinks", "business", "tickets", "gift", "gas"]
cmds = ["pay","linkbank","override","request","transfer","deposit","acceptrequest","unrequest","denyrequest","friend","balance","adduser","verify","unfriend","setprivacy","updateprivacy","transactionprivacy","globallog","friendlog","personallog","requestlog","viewprofile"]

### HELPER FUNCTIONS ###

def fetch(fetchone):
    return str(''.join(fetchone))

def isverified(userID,cursor):
    cursor.execute(''' SELECT ssn FROM users WHERE username=?''',(userID,))
    ssn = fetch(cursor.fetchone())
    if ssn == "*":
        print("Error: User is not verified.")
        return False
    return True

#isverified no print    
def isVerified(userID,cursor):
    cursor.execute(''' SELECT ssn FROM users WHERE username=?''',(userID,))
    ssn = fetch(cursor.fetchone())
    if ssn == "*":
        return False
    return True

#Checks if user inputs correct password
def passwordchecker(userID,password,cursor):
    cursor.execute( ''' SELECT password FROM users WHERE username=?''',(userID,))
    correctpassword = str(''.join(cursor.fetchone()))
    if password != correctpassword:
        print("Error: Incorrect password.")
        print("======\nPassword requirements: At least 8 characters length, including at least one uppercase letter, one lowercase letter, and one number.")
        return False
    return True

#Accesses current user balance
def getbalance(userID,cursor):
    cursor.execute(''' SELECT balance FROM users WHERE username=? ''', (userID,))
    userBalance = str(cursor.fetchone()).replace("(","").replace(")","").replace(",","")
    userBalance = float(userBalance)
    return userBalance

#Accesses total user fees
def getfees(userID, cursor):
    cursor.execute(''' SELECT fees FROM users WHERE username=? ''', (userID,))
    userFees = str(cursor.fetchone()).replace("(","").replace(")","").replace(",","")
    userFees = float(userFees)
    return userFees

#checks if a user currently exists
def validateuser(userID,cursor):
    cursor.execute(''' SELECT username FROM users WHERE username=?''', (userID,))
    if cursor.fetchone() == None:
        print(f"Error: User {userID} not in system.")
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

#takes in user ID and returns list of their friends.
def friendgetter(userID, cursor):
    cursor.execute(''' SELECT friends FROM users WHERE username=?''',(userID,))
    return ''.join(cursor.fetchone()).split(',')

#Checks if user has friended another user and/or if the other user has friended them back
def friendchecker(senderID,recipientID,cursor):
    senderFriends = friendgetter(senderID,cursor)
    if recipientID not in senderFriends:
        print("Error: You are not friends with " + recipientID + ".")
        return False
    recipientFriends = friendgetter(recipientID,cursor)
    if senderID not in recipientFriends:
        print("Error: " + recipientID + " has not friended you back.")
        return False
    return True

#Checks if user has friended another user and/or if the other user has friended them back. Does not print anything.
def friendcheck(senderID,recipientID,cursor):
    senderFriends = friendgetter(senderID,cursor)
    if recipientID not in senderFriends:
        return False
    recipientFriends = friendgetter(recipientID,cursor)
    if senderID not in recipientFriends:
        return False
    return True

#function takes a user and a command and determines if they have crossed the Venmo limit for that command
def limitenforcer(userID,cmd,amount,cursor):
    #possible inputs for cmd: "pay", "request", "transfer", "deposit"
    #make sure user exists
    if not validateuser:
        return

    #fetch user type
    cursor.execute(''' SELECT accounttype FROM users WHERE username=?''',(userID,))
    accountType = fetch(cursor.fetchone())

    #figure out if user is verified or not
    cursor.execute(''' SELECT ssn FROM users WHERE username=?''',(userID,))
    ssn = fetch(cursor.fetchone())
    verified = ssn != "*"

    #get the date from one week ago
    oneweekago = datetime.now() - timedelta(7)

    #set (v) verified and (u) unverified limits for (p) personal and (b) business accounts
    p_unverifiedlimit = 299.99
    p_verifiedlimit = 6999.99
    b_unverifiedlimit = 2499.99
    b_verifiedlimit = 24999.99
    p_maxpayment = 4999.99
    p_utransferlim = 999.99
    p_vtransferlim = 19999.99
    b_utransferlim = 999.99
    b_vtransferlim = 49999.99
    p_maxdeposit = 1500.00
    b_maxtransfer = 10000.00

    #figure how much the user has paid out in the last week and check if it exceeds any limits
    if cmd == "pay":
        cursor.execute(''' SELECT SUM(amount) FROM paymentLog WHERE senderID=? AND date>=? AND status=? ''',(userID,oneweekago,"_payment"))
        try:
            amountspent = float(str(cursor.fetchone()).replace("(","").replace(")","").replace(",",""))
        except ValueError:
            amountspent = 0
        if accountType =="Personal":
            if amount > p_maxpayment:
                print(f"Error: Payment amount exceeds max {accountType} payment amount of ${p_maxpayment}.")
                return False
            if (not verified) and ((amountspent + amount) > p_unverifiedlimit):
                print(f"Error: This week, you have already spent ${amountspent}. This payment would cause {userID} to exceed the weekly unverified {accountType} payment limit of ${p_unverifiedlimit} by:")
                print(f"${round(amountspent + amount - p_unverifiedlimit,2)}")
                return False
            elif (verified) and ((amountspent + amount) > p_verifiedlimit):
                print(f"Error: This week, you have already spent ${amountspent}. This payment would cause {userID} to exceed the weekly verified {accountType} payment limit of $${p_verifiedlimit} by:")
                print(f"${round(amountspent + amount - p_verifiedlimit,2)}")
                return False
        elif accountType =="Business":
            if (not verified) and ((amountspent + amount) > b_unverifiedlimit):
                print(f"Error: This week, you have already spent ${amountspent}. This payment would cause {userID} to exceed the weekly unverified {accountType} payment limit of ${b_unverifiedlimit} by:")
                print(f"${round(amountspent + amount - b_unverifiedlimit,2)}")
                return False
            elif (verified) and ((amountspent + amount) > b_verifiedlimit):
                print(f"Error: This week, you have already spent ${amountspent}. This payment would cause {userID} to exceed the weekly verified {accountType} payment limit of ${b_verifiedlimit} by:")
                print(f"${round(amountspent + amount - b_verifiedlimit,2)}")
                return False
    #Checks if request is asking for a too large amount
    elif cmd == "request":
        if accountType == "Personal" and (amount > p_maxpayment):
            print(f"Error: You cannot request an amount higher than ${p_maxpayment}")
            return False
    #checks if user has exceeded weekly transfer limit
    elif cmd == "transfer":
        cursor.execute(''' SELECT SUM(amount) FROM paymentLog WHERE senderID=? AND date>=? AND status=? ''',(userID,oneweekago,"transfer"))
        try:
            amounttransferred = float(str(cursor.fetchone()).replace("(","").replace(")","").replace(",",""))
        except ValueError:
            amounttransferred = 0
        if accountType == "Personal":
            if (not verified) and ((amounttransferred + amount) > p_utransferlim):
                print(f"Error: This week, you have already transferred ${amounttransferred}. This transfer would cause {userID} to exceed the weekly unverified {accountType} transfer limit of ${p_utransferlim} by:")
                print(f"${round(amounttransferred + amount - p_utransferlim,2)}")
                return False
            elif (verified) and ((amounttransferred + amount) > p_vtransferlim):
                print(f"Error: This week, you have already transferred ${amounttransferred}. This transfer would cause {userID} to exceed the weekly unverified {accountType} transfer limit of ${p_vtransferlim} by:")
                print(f"${round(amounttransferred + amount - p_vtransferlim,2)}")
                return False
        elif accountType == "Business":
            if (amount > b_maxtransfer):
                print(f"Error: The attempted transfer exceeds the maximum amount allowed for a {accountType} transfer of {b_maxtransfer} by:")
                print(f"${amount - b_maxtransfer}")
                return False
            if (not verified) and ((amounttransferred + amount) > b_utransferlim):
                print(f"Error: This week, you have already transferred ${amounttransferred}. This transfer would cause {userID} to exceed the weekly unverified {accountType} transfer limit of ${b_utransferlim} by:")
                print(f"${round(amounttransferred + amount - b_utransferlim,2)}")
                return False
            elif (verified) and ((amounttransferred + amount) > b_vtransferlim):
                print(f"Error: This week, you have already transferred ${amounttransferred}. This transfer would cause {userID} to exceed the weekly unverified {accountType} transfer limit of ${b_vtransferlim} by:")
                print(f"${round(amounttransferred + amount - b_vtransferlim,2)}")
                return False
    elif cmd == "deposit" and accountType == "Personal":
        if amount > p_maxdeposit:
            print(f"Error: You cannot deposit more than ${p_maxdeposit} at once.")
            return False

    return True

def checkusername(userID):
    bannedchars = [",","(",")","*","."]
    errormessage = ""
    for char in userID:
        if char in bannedchars:
            bannedchars.remove(char)
            if len(errormessage) == 0:
                errormessage = errormessage + "'" + char + "'"
            else:
                errormessage = errormessage + " and " + "'" + char + "'"
    if len(errormessage) != 0:
        print(f"Error: Invalid username. Please remove {errormessage} from the username. ")
        return False
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


### CORE FUNCTIONS ###

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
    if senderID==recipientID:
        print("Error: You can't pay yourself!")
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

    if not limitenforcer(senderID, "pay", amount, cursor):
        return

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

    #fee for business accounts when receiving a payment
    fee = 0
    cursor.execute(''' SELECT accounttype FROM users WHERE username=?''',(recipientID,))
    accountType = fetch(cursor.fetchone())
    if (amount > 1) and accountType == "Business":
        fee = (amount * 0.019) + 0.1

    # hashing function to generate payment ID
    paymentID = hash(str(senderID)+str(recipientID)+str(message)+str(datetime.now()))

    #updating user balance
    senderBalance = senderBalance - amount
    recipientBalance = recipientBalance + amount - fee
    cursor.execute(''' UPDATE users SET balance = ? WHERE username=? ''',(senderBalance,senderID))
    cursor.execute(''' UPDATE users SET balance = ? WHERE username=? ''',(recipientBalance,recipientID))
    cursor.execute(''' UPDATE users SET fees = fees + ? WHERE username=? ''',(fee,recipientID))
    cursor.execute(''' INSERT INTO paymentLog (senderID, recipientID, amount, status, date, message, paymentID, privacy, tag, senderBalance, recipientBalance)
    VALUES (?,?,?,?,?,?,?,?,?,?,?) ''',(senderID,recipientID,amount,"_payment",datetime.now(),message.strip('"'),paymentID,privacy,tag,senderBalance,recipientBalance))
    twodecimalformatting = "{:.2f}"
    print(f"Successfuly paid {recipientID} ${twodecimalformatting.format(amount)}!")
    if fee > 0:
        print(f"{recipientID} was charged a {accountType} account fee of ${twodecimalformatting.format(fee)} for this transaction, so ${twodecimalformatting.format(amount-fee)} was added to their balance.")
    return True

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
    else:
        return
    
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
    
    print(f"Successfully changed {userID}'s bank from {oldbank} to {bankID}.")
    

def request(userID, friendID,amount,message,cursor,tag=None):
    #checks if user exists
    if not validateuser(userID,cursor):
        return
    
    if userID == friendID:
        print("Error: You can't request yourself!")
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

    if not limitenforcer(userID, "request", amount, cursor):
        return

    if tag != None and tag.lower().strip() not in tags:
        print(f"Error: Invalid tag. Valid tags are:\n {tags}")
        return False

    #generates requestID
    requestID = hash(str(userID)+str(friendID)+str(message)+str(datetime.now()))

    cursor.execute(''' INSERT INTO paymentLog (senderID, recipientID, amount, status, date, message, paymentID, privacy, tag, senderBalance, recipientBalance)
    VALUES (?,?,?,?,?,?,?,?,?,?,?) ''',(friendID,userID,amount,"request",datetime.now(),message.strip('"'),requestID,None,tag,None,None))
    twodecimalformatting = "{:.2f}"
    amount = twodecimalformatting.format(amount)
    print(f"Successfully requested ${amount} from {friendID}.")

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
        elif request_status == "transfer":
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
            print(f"Request {paymentID} successfully cancelled.")
        elif request_status == "cancelled_request":
            print("Error: User already cancelled this request.")
        elif request_status == "denied_request":
            print("Error: This request was already denied.")
        elif request_status == "accepted_request":
            print("Error: This request was already accepted.")
        elif request_status =="_payment":
            print("Error: This payment ID corresponds to a payment, not a request.")
            return
        elif request_status == "transfer":
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
            print(f"Request denied for request ID {paymentID}.")
        elif request_status == "cancelled_request":
            print("Error: This request was already cancelled.")
        elif request_status =="denied_request":
            print("Error: You already denied this request.")
        elif request_status =="accepted_request":
            print("Error: You already accepted this request.")
        elif request_status =="_payment":
            print("Error: This payment ID corresponds to a payment, not a request.")
            return
        elif request_status == "transfer":
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
            print("Error: You cannot deposit zero dollars or a negative amount of money into your Venmo.")
            return
    except ValueError:
        print("Error: Did not input a numerical amount.")
        return
    cursor.execute( ''' SELECT bank FROM users WHERE username=?''',(userID,))
    bankID = str(''.join(cursor.fetchone()))
    if bankID == "*":
        print("Error: You do not have bank account set up.\nUse linkBank to add your information.")
        return

    if not limitenforcer(userID, "deposit", amount, cursor):
        return

    userBalance = getbalance(userID,cursor)
    userBalance += amount
    cursor.execute( ''' UPDATE users SET balance=? WHERE username =?''',(userBalance,userID))
    twodecimalformatting = "{:.2f}"
    print(f"Successfully deposited ${twodecimalformatting.format(amount)} in {userID}'s account from bank {bankID}.")
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
        print(f"Error: You cannot transfer more than you have in your account. Current balance: {userBalance + amount}.")
        return

    if not limitenforcer(userID, "transfer", amount, cursor):
        return

    if amount < 0.25 and type == "Instant Transfer":
        print("Error: The minimum transfer amount for instant transfers is 0.25.")
    #Updating users 
    cursor.execute(''' UPDATE users SET balance=? WHERE username=?''',(userBalance,userID))
    cursor.execute(''' UPDATE users SET fees=fees+? WHERE username=?''',(fee,userID))
    
    #generating transfer ID
    transferID = hash(str(userID)+str(userBank)+str(type)+str(datetime.now()))
    print(f"${amount} transferred to Bank: {userBank}. Your new balance is ${userBalance}.")
    if fee > 0:
        print(f"Your fee for this transfer was: ${fee}")

    #updating paymentLog
    cursor.execute(''' INSERT INTO paymentLog (senderID, recipientID, amount, status, date, message, paymentID, privacy, tag, senderBalance, recipientBalance)
    VALUES (?,?,?,?,?,?,?,?,?,?,?) ''',(userID,userBank,amount,"transfer",datetime.now(),type,transferID,None,None,None,None))


    return

def friend(userID, friendID, cursor):
    if not validateuser(userID,cursor):
        return

    if userID == friendID:
        print("Error: You cannot friend yourself!")
        return

    cursor.execute(''' SELECT username FROM users WHERE username=?''', (friendID,))
    if cursor.fetchone() == None:
        print("Error: No account exists with " + friendID + " as its username.")
        return

    listoffriends = friendgetter(userID,cursor)
    cursor.execute(''' SELECT friends FROM users WHERE username=?''', (userID,))
    currentFriends = fetch(cursor.fetchone()) 

    if friendID in listoffriends:
        print("Error: You are already friends with " + friendID + ".")
        return

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
    
    print(f"{userID} and {friendID} are no longer friends.")

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
    print(f"Successfully set {userID}'s privacy to {privacy}.")
    

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

    #makes sure certain characters aren't in the username
    if not checkusername(userID):
        return
    if not checkpassword(password):
        return

    #calculating and reformatting the current date
    date = str(datetime.now())
    date = date[0:10]

    cursor.execute(''' INSERT INTO users (username, friends, balance, accounttype, password, creationDate) 
    VALUES (?,?,?,?,?,?) ''',
    (userID, "*", 0.0, accountType, password, date))
    print(f"Account has been successfully created.\nUserID: {userID}\nPassword: {password}")
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

def globallog(cursor,userID,below=False,above=False,sender=False,recipient=False,olddate=False,messagefilter=False,rangeupper=False,rangelower=False,tagfilter=False,messagecontains=False):
    if not validateuser(userID,cursor):
        return
    
    #getting list of user's friends to track Friends Only transactions
    cursor.execute(''' SELECT friends FROM users WHERE username=?''', (userID,))
    userFriends = fetch(cursor.fetchone())
    userFriends = userFriends.split(",")

    #filtering the database for globally visible payments to userID (Public,  Friends Only involving their friends, and all transactions involving userID)
    cursor.execute(''' SELECT paymentID FROM paymentLog ''') 
    log = cursor.fetchall()
    if (log == None):
        print("The global log is currently empty. There are no records of Public transactions.")
        return
    else:
        notemptylog = False
        counter = 1
        for elem in log:
            #get the paymentID
            paymentID = fetch(elem)

            #get the payment status
            cursor.execute(''' SELECT status FROM paymentLog WHERE rowid = ?''', (counter,))
            status = fetch(cursor.fetchone())

            #if the paymennt is a transfer or request, continue
            if status != "_payment":
                counter += 1
                continue

            #get privacy
            cursor.execute(''' SELECT privacy FROM paymentLog WHERE rowid = ?''', (counter,))
            try:
                privacy = fetch(cursor.fetchone())
            except TypeError:
                privacy = None
            
            #get senderID
            cursor.execute(''' SELECT senderID FROM paymentLog WHERE rowid = ?''', (counter,))
            senderID = fetch(cursor.fetchone())
            
            #get recipientID
            cursor.execute(''' SELECT recipientID FROM paymentLog WHERE rowid = ?''', (counter,))
            recipientID = fetch(cursor.fetchone())

            #privacy is public, friends only and ur friends with one, ur in the transaction
            cond1 = privacy == "Public"
            cond2 = privacy == "Friends Only" and (friendcheck(userID, senderID, cursor) or friendcheck(userID, recipientID, cursor))
            cond3 = senderID == userID or recipientID == userID
            if not (cond1 or cond2 or cond3):
                counter += 1
                continue

            #apply sender/recipient filters
            if (sender != False) and (sender.lower() != senderID.lower()):
                counter+=1
                continue
            if (recipient != False) and (recipient.lower() != recipientID.lower()):
                counter+=1
                continue

            #get message
            cursor.execute(''' SELECT message FROM paymentLog WHERE rowid = ?''', (counter,))
            message = fetch(cursor.fetchone())

            #apply message / messagecontains filters
            if (messagefilter !=False) and (messagefilter.lower() != message.lower()):
                counter+=1
                continue

            if (messagecontains != False) and (messagecontains.lower() not in message.lower()):
                counter+=1
                continue

            #get date
            cursor.execute(''' SELECT date FROM paymentLog WHERE rowid = ?''', (counter,))
            date = fetch(cursor.fetchone())
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
            
            #apply date filter
            if olddate!=False and (date < olddate):
                counter+=1
                continue

            #get tag
            cursor.execute(''' SELECT tag FROM paymentLog WHERE rowid = ?''', (counter,))
            try:
                tag = fetch(cursor.fetchone())
            except TypeError:
                tag = None
        
            #apply tag filter
            if tagfilter !=False and (tag != tagfilter):
                counter+=1
                continue

            #get amount
            cursor.execute(''' SELECT amount FROM paymentLog WHERE rowid = ?''', (counter,))
            amount = float(str(cursor.fetchone()).replace("(","").replace(")","").replace(",",""))

            #apply below/above/range filters
            if below !=False and amount >= below:
                counter+=1
                continue

            if above !=False and amount <= above:
                counter+=1
                continue

            if (rangeupper != False) and (amount > rangeupper or amount < rangelower):
                counter+=1
                continue

            #printing the payment to the log
            print("======")
            twodecimalformatting = "{:.2f}"
            print(f"{senderID.upper()} paid {recipientID.upper()} ${twodecimalformatting.format(amount)}")
            date = str(date)
            date = date[0:19]
            print(f"Date: {date}")
            print(f"Message: {message}")
            print(f"ID: {paymentID}")
            if privacy != None:
                print(f"Privacy: {privacy}")
            if tag != None:
                print(f"Tag: {tag}")
            print("======\n")
            notemptylog = True

            counter += 1
    if not notemptylog:
        print("======")
        print("No recorded payments were found matching the provided filters.")
        print("======\n")


def friendlog(cursor,userID,friendID,below=False,above=False,sender=False,recipient=False,olddate=False,messagefilter=False,rangeupper=False,rangelower=False,tagfilter=False,messagecontains=False):
    if not validateuser(userID,cursor):
        return
    if not validateuser(friendID,cursor):
        return
    if not friendchecker(userID,friendID,cursor):
        return
    #Fetches all relevant information from payments under the following conditions
    #Either the sender or recipient is the friend AND the privacy is public or friends only.
    #Either the sender or recipient is the friend AND either the friend or recipient is the user
    #Filters out all requests, only displays actual payments
    cursor.execute(''' SELECT senderID, recipientID, amount, date, message, paymentID, privacy, tag FROM paymentLog WHERE ((senderID=? OR recipientID=?) AND status=? AND (privacy=? OR privacy=?))
    OR (status=? AND (senderID=? OR recipientID=?) AND (senderID=? OR recipientID=?)) ''',(friendID,friendID,"_payment","Public","Friends Only","_payment",friendID,friendID,userID,userID))
    log = cursor.fetchall()
    if (log == None):
        print(f"There are no transactions in the system involving {friendID}.")
        return
    notemptylog = False
    for elem in log:  
        senderID = elem[0]
        recipientID = elem[1]
        amount = elem[2]
        date = elem[3]
        #redefing date as a datetime
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        message = elem[4]
        paymentID = elem[5]
        privacy = elem[6]
        tag = elem[7]

        #apply sender/recipient filters
        if (sender != False) and (sender.lower() != senderID.lower()):
            continue
        if (recipient != False) and (recipient.lower() != recipientID.lower()):
            continue

        #apply message / messagecontains filters
        if (messagefilter !=False) and (messagefilter.lower() != message.lower()):
            continue

        if (messagecontains != False) and (messagecontains.lower() not in message.lower()):
            continue
        
        #apply date filter
        if olddate!=False and (date < olddate):
            continue

        #apply tag filter False == None
        if tagfilter !=False and (tag != tagfilter):
            continue

        #apply below/above/range filters
        if below !=False and amount >= below:
            continue

        if above !=False and amount <= above:
            continue

        if (rangeupper != False) and (amount > rangeupper or amount < rangelower):
            continue

        #printing the payment to the log
        print("=======")
        twodecimalformatting = "{:.2f}"
        print(f"{senderID.upper()} paid {recipientID.upper()} ${twodecimalformatting.format(amount)}")
        date = str(date)
        date = date[0:19]
        print(f"Date: {date}")
        print(f"Message: {message}")
        print(f"ID: {paymentID}")
        if privacy != None:
            print(f"Privacy: {privacy}")
        if tag != None:
            print(f"Tag: {tag}")
        print("=======\n")
        notemptylog = True

    if not notemptylog:
        print("======")
        print("No recorded payments were found matching the provided filters.")
        print("======\n")
    return

def personallog(cursor,userID,below=False,above=False,sender=False,recipient=False,olddate=False,messagefilter=False,rangeupper=False,rangelower=False,tagfilter=False,messagecontains=False,transfersonly=False,paymentsonly=False):
    cursor.execute(''' SELECT senderID, recipientID, amount, date, status, message, tag,privacy, paymentID FROM paymentLog WHERE
    (senderID=? OR recipientID=?) AND (status=? OR status=?)
    ''',(userID,userID,"_payment","transfer"))
    log = cursor.fetchall()
    if (log == None):
        print(f"There are no transactions in the system involving {userID}.")
        return
    notemptylog = False
    for elem in log:
        senderID = elem[0]
        recipientID = elem[1]
        amount = elem[2]
        date = elem[3]
        #redefing date as a datetime
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        status = elem[4]
        message = elem[5]
        tag = elem[6]
        privacy = elem[7]
        paymentID = elem[8]

        #apply sender/recipient filters
        if (sender != False) and (sender.lower() != senderID.lower()):
            continue
        if (recipient != False) and (recipient.lower() != recipientID.lower()):
            continue

        #apply message / messagecontains filters
        if (messagefilter !=False) and (messagefilter.lower() != message.lower()):
            continue

        if (messagecontains != False) and (messagecontains.lower() not in message.lower()):
            continue
        
        #apply date filter
        if olddate!=False and (date < olddate):
            continue

        #apply tag filter False == None
        if tagfilter !=False and (tag != tagfilter):
            continue

        #apply below/above/range filters
        if below !=False and amount >= below:
            continue

        if above !=False and amount <= above:
            continue

        if (rangeupper != False) and (amount > rangeupper or amount < rangelower):
            continue

        #apply transferonly/paymentsonly filter
        if transfersonly and status != "transfer":
            continue
        if paymentsonly and status != "_payment":
            continue

        #printing the payment to the log
        print("=======")
        twodecimalformatting = "{:.2f}"
        if status == "_payment":
            print(f"{senderID.upper()} paid {recipientID.upper()} ${twodecimalformatting.format(amount)}")
        if status == "transfer":
            print(f"{senderID.upper()} transferred ${twodecimalformatting.format(amount)} to bank {recipientID}")
            print(f"{message}")
        date = str(date)
        date = date[0:19]
        print(f"Date: {date}")
        if status =="_payment":
            print(f"Message: {message}")
        print(f"ID: {paymentID}")
        if privacy != None:
            print(f"Privacy: {privacy}")
        if tag != None:
            print(f"Tag: {tag}")
        print("=======\n")
        notemptylog = True

    if not notemptylog:
        print("======")
        print("No recorded payments were found matching the provided filters.")
        print("======\n")
    return

def requestlog(cursor,userID,below=False,above=False,incoming=False,outgoing=False,requester=False,requested=False,olddate=False,messagefilter=False,rangeupper=False,rangelower=False,tagfilter=False,messagecontains=False,statusfilter=False):
    #Selecting all requests where the user is involved as either a sender or recipient
    cursor.execute(''' SELECT senderID, recipientID, amount, date, status, message,tag,paymentID FROM paymentLog WHERE
    (status=? OR status=? OR status=? OR status=?) AND
    (senderID=? OR recipientID=?)
     ''',("request","accepted_request","cancelled_request","denied_request",userID,userID))
    log = cursor.fetchall()
    if (log == None):
        print(f"There are no requests in the system involving {userID}.")
        return
    notemptylog = False

    for elem in log:
        senderID = elem[0]
        recipientID = elem[1]
        amount = elem[2]
        date = elem[3]
        #reformatting date as datetime
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        status = elem[4]
        message = elem[5]
        tag = elem[6]
        paymentID = elem[7]
        #apply incoming/outgoing filters

        if (incoming) and (senderID.lower() != userID.lower()):
            continue
        if (outgoing) and (recipientID.lower() != userID.lower()):
            continue

        #apply sender/recipient filters
        if (requested != False) and (requested.lower() != senderID.lower()):
            continue
        if (requester != False) and (requester.lower() != recipientID.lower()):
            continue

        #apply message / messagecontains filters
        if (messagefilter !=False) and (messagefilter.lower() != message.lower()):
            continue

        if (messagecontains != False) and (messagecontains.lower() not in message.lower()):
            continue
        
        #apply date filter
        if olddate!=False and (date < olddate):
            continue

        #apply tag filter False == None
        if tagfilter !=False and (tag != tagfilter):
            continue

        #apply below/above/range filters
        if below !=False and amount >= below:
            continue

        if above !=False and amount <= above:
            continue

        if (rangeupper != False) and (amount > rangeupper or amount < rangelower):
            continue

        #apply status filter
        if statusfilter != False and statusfilter != status:
            continue

        #printing the payment to the log
        print("===============")
        twodecimalformatting = "{:.2f}"
        if status == "request":
            print("PENDING REQUEST")
            print(f"{recipientID.upper()} requested {twodecimalformatting.format(amount)} from {senderID.upper()}")
        elif status == "accepted_request":
            print(f"{senderID.upper()} accepted {recipientID.upper()}'s request for {twodecimalformatting.format(amount)}")
        elif status == "denied_request":
            print("DENIED REQUEST")
            print(f"{senderID.upper()} denied {recipientID.upper()}'s request for {twodecimalformatting.format(amount)}")
        elif status == "cancelled_request":
            print("CANCELLED REQUEST")
            print(f"{recipientID.upper()} requested {twodecimalformatting.format(amount)} from {senderID.upper()}")
        date = str(date)
        date = date[0:19]
        print(f"Date: {date}")
        print(f"Message: {message}")
        print(f"ID: {paymentID}")
        if tag != None:
            print(f"Tag: {tag}")
        print("===============\n")
        notemptylog = True

    if not notemptylog:
        print("======")
        print("No recorded payments were found matching the provided filters.")
        print("======\n")
    return

def viewprofile(cursor, userID):
    if not validateuser(userID, cursor):
        return
    #fetching profile information
    balance = getbalance(userID, cursor)
    fees = getfees(userID, cursor)
    numFriends = len(friendgetter(userID, cursor))
    if (numFriends == 1) and friendgetter(userID, cursor) == ["*"]:
        numFriends = 0
    verified = isVerified(userID, cursor)
    cursor.execute(''' SELECT creationDate FROM users WHERE username=?''', (userID,))
    date = fetch(cursor.fetchone())

    #printing the profile
    print("==================")
    print("VENMO User Profile")
    print("==================")
    if verified:
        print(f"@{userID.upper()} - √erified")
    else:
        print(f"@{userID.upper()} - unverified")
    #Reformatting balance
    balance = "{:.2f}".format(balance)
    print(f"${balance}")
    if numFriends == 0:
        print("No friends yet!") 
    elif (numFriends == 1):
        print(f"{numFriends} friend")
    else:
        print(f"{numFriends} friends")
    if fees > 0:
        #Reformatting fees
        fees = "{:.2f}".format(fees)
        print(f"ƒees: ${fees}")
    print(f"joined {date}")
    print("==================")
    return


### INPUT VALIDATER ###

def inputvalidater(argv,cursor):
    if len(argv) == 1:
        print("Please enter a command.")
        print(f"Possible commands: {cmds}")
        return

    command = argv[1].lower()
    filters = ["-above","-below","-range","-days","-tags","-sender","-recipient","-message","-messagecontains"]
    
    if command not in cmds:
        print("Please enter a valid command.")
        print(f"Possible commands: {cmds}")
        return

    if command == "globallog":
        if len(argv) == 2:
            print("Usage: globallog userID [filters]")
            print(f"Possible filters: {filters}")
            return
        userID = argv[2].lower()
        if len(argv) == 3:
            globallog(cursor,userID)
            return
        above = False
        below = False
        olddate = False
        rangeupper = False
        rangelower = False
        tag = False
        sender = False
        recipient = False
        message = False
        messagecontains = False


        for i in range(3,len(argv),1):
            if (i%2==1) and argv[i].lower() not in filters:
            #makes sure user is inputting valid filters
                print(f"Error: Invalid filter: {argv[i]}.")
                print("Usage: globallog userID [filters]")
                print(f"Possible filters: {filters}")
                return
            #filters commands are not case sensitive
            if (i%2 ==1):
                argv[i] = argv[i].lower()
            if argv[i] == "-above":
                if below != False:
                    print("Error: You cannot use -above and -below simultaneously. Instead, use -range")
                    return
                if above != False:
                    print("Error: You cannot use -above more than once.")
                    return
                try:
                    above = argv[i+1]
                except IndexError:
                    print("Error: Please enter an amount after -above.")
                    return
                try:
                    above = float(above)
                    if above <0:
                        print("Error: You cannot enter an amount lower than 0.")
                        return
                except ValueError:
                    print("Error: Please enter a numerical amount after -above.")
                    return
                
            if argv[i] == "-below":
                if above != False:
                    print("Error: You cannot use -above and -below simultaneously.")
                    return
                if below != False:
                    print("Error: You cannot use -below more than once.")
                    return
                try:
                    below = argv[i+1]
                except IndexError:
                    print("Error: Please enter an amount after -below.")
                    return
                try:
                    below = float(below)
                except ValueError:
                    print("Error: Please enter a numerical amount after -below.")
                    return
                if below <= 0:
                    print("Error: Amount below must be greater than 0.")
                    return
            if argv[i] == "-range":
                if rangeupper != False:
                    print("Error: You cannot use -range more than once.")
                    return
                try:
                    numberrange = argv[i+1]
                except IndexError:
                    print("Error: Please enter an interval (Example: 1-100) after -range.")
                    return
                if re.match("\\d+-\\d+",numberrange) == None:
                    print("Error: Please enter an interval (Example: 1-100) after -range.")
                    return
                numberrange = numberrange.split("-")                
                rangelower = float(numberrange[0])
                rangeupper = float(numberrange[1])
                if rangelower >= rangeupper:
                    print("Error: Invalid interval range. Upper bound of range must exceed the lower bound.")
            if argv[i] == "-days":
                if olddate != False:
                    print("Error: You cannot use -days more than once.")
                    return
                
                try:
                    days = argv[i+1]
                except IndexError:
                    print("Error: Please enter a number of days after -days.")
                    return
                try:
                    days = int(days)
                except ValueError:
                    print("Error: Please enter an integer amount of days after -days.")
                    return
                if days <= 0:
                    print("Error: Amount of days must be at least one.")
                    return
                
                #get the date from when the user wants 
                olddate = datetime.now() - timedelta(days)
        
            if argv[i] == "-tags":
                if tag != False:
                    print("Error: You cannot use -tags more than once.")
                    return

                try:
                    tag = argv[i+1]
                except IndexError:
                    print("Error: Please enter tag after -tags.")
                    return
                try:
                    tag = tag.lower()
                except SyntaxError:
                    print("Error: Please enter a valid tag. Valid tags are:\n {tags}")
                    return
                if tag.lower() not in tags:
                    print(f"Error: Invalid tag. Valid tags are:\n {tags}")
                    return

            if argv[i] == "-sender":
                if sender != False:
                    print("Error: You cannot use -sender more than once.")
                    return
                try:
                    sender = argv[i+1]
                except IndexError:
                    print("Error: Please enter sender after -sender.")
                    return


            if argv[i] == "-recipient":
                if recipient != False:
                    print("Error: You cannot use -recipient more than once.")
                    return
                try:
                    recipient = argv[i+1]
                except IndexError:
                    print("Error: Please enter recipient after -recipient.")
                    return

            if argv[i] == "-message":
                if message != False:
                    print("Error: You cannot use -message more than once.")
                    return
                try:
                    message = argv[i+1]
                except IndexError:
                    print("Error: Please enter message after -message.")
                    return

            if argv[i] == "-messagecontains":
                if messagecontains != False:
                    print("Error: You cannot use -message more than once.")
                    return
                try:
                    messagecontains = argv[i+1]
                except IndexError:
                    print("Error: Please enter message after -messagecontains.")
                    return
        globallog(cursor,userID,below,above,sender,recipient,olddate,message,rangeupper,rangelower,tag,messagecontains)
        return
    if command == "pay":
        #function takes: pay senderID recipientID amount message cursor -tag -privacy
        #venmo.py pay senderID recipientID amount message -tag -privacy
        if len(argv) != 6 and len(argv) != 8 and len(argv) != 10:
            print("Error: Incorrect usage of pay.")
            print("Usage: venmo.py pay senderID recipientID amount message [-tag tag -privacy privacy]")
            return
        senderID = argv[2].lower()
        recipientID = argv[3].lower()
        amount = argv[4]
        message = argv[5]
        if len(argv) == 6:
            pay(senderID,recipientID,amount,message,cursor)
            return
        privacy = None
        tag = None
        if len(argv) == 8:
            if argv[6] != "-privacy" and argv[6] != "-tag":
                print("Error: Incorrect usage of pay.")
                print("Usage: venmo.py pay senderID recipientID amount message [-tag tag -privacy privacy]")
                return
            if argv[6] == "-privacy":
                privacy = argv[7]
            if argv[6] == "-tag": 
                tag = argv[7]
            pay(senderID,recipientID,amount,message,cursor,tag,privacy)
        if len(argv) == 10:
            for i in range(6,len(argv),1):
                if argv[i] == "-privacy":
                    if privacy != None:
                        print("Error: You cannot use -privacy more than once.")
                        return
                    try:
                        privacy = argv[i+1]
                    except IndexError:
                        print("Error: Incorrect usage of pay.")
                        print("Usage: venmo.py pay senderID recipientID amount message [-tag tag -privacy privacy]")
                        return
                if argv[i] == "-tag":
                    if tag != None:
                        print("Error: You cannot use -tag more than once.")
                        return
                    try:
                        tag = argv[i+1]
                    except IndexError:
                        print("Error: Incorrect usage of pay.")
                        print("Usage: venmo.py pay senderID recipientID amount message [-tag tag -privacy privacy]")
                        return
            pay(senderID,recipientID,amount,message,cursor,tag,privacy)
        return
    if command == "request":
        #request userID friendID amount message [-tag tag]
        if len(argv) != 6 and len(argv) != 8:
            print("Error: Incorrect usage of request.")
            print("Usage: venmo.py request userID friendID amount message [-tag tag]")
            return
        senderID = argv[2].lower()
        recipientID = argv[3].lower()
        amount = argv[4]
        message = argv[5]
        if len(argv) == 6:
            request(senderID,recipientID,amount,message,cursor)
            return
        if len(argv) == 8:
            if argv[6] != "-tag":
                print("Error: Incorrect usage of request.")
                print("Usage: venmo.py request userID friendID amount message [-tag tag]")
                return
            request(senderID,recipientID,amount,message,cursor,argv[7])
        return
    if command == "acceptrequest":
        #venmo.py acceptRequest senderID paymentID [-privacy privacy]
        if len(argv) != 4 and len(argv) != 6:
            print("Error: Incorrect usage of acceptrequest.")
            print("Usage: venmo.py acceptrequest senderID paymentID [-privacy privacy]")
            return
        senderID = argv[2].lower()
        paymentID = argv[3]
        if len(argv) ==4:
            acceptrequest(senderID,paymentID,cursor)
            return
        if argv[4] != "-privacy":
            print("Error: Incorrect usage of acceptrequest.")
            print("Usage: venmo.py acceptrequest senderID paymentID [-privacy privacy]")
            return
        privacy = argv[5]
        acceptrequest(senderID,paymentID,cursor,privacy)
        return
    if command == "unrequest":
        if len(argv) != 4:
            print("Error: Incorrect usage of unrequest.")
            print("Usage: venmo.py unrequest userID paymentID")
            return
        unrequest(argv[2].lower(),argv[3],cursor)
    if command == "denyrequest":
        if len(argv) != 4:
            print("Error: Incorrect usage of denyrequest.")
            print("Usage: denyrequest senderID paymentID")
            return
        denyrequest(argv[2].lower(),argv[3],cursor)
        return
    if command == "deposit":
        if len(argv) != 4:
            print("Error: Incorrect usage of deposit.")
            print("Usage: deposit userID amount")
            return
        deposit(argv[2].lower(),argv[3],cursor)
        return
    if command == "transfer":
        if len(argv) != 4 and len(argv) != 6:
            print("Error: Incorrect usage of transfer.")
            print('Usage: transfer userID amount [-type instant or -type "no fee"]')
            return
        if len(argv) == 4:
            transfer(argv[2].lower(),argv[3],cursor)
            return
        if len(argv) == 6:
            if argv[4] != "-type":
                print("Error: Incorrect usage of transfer.")
                print('Usage: transfer userID amount [-type Instant or -type "No Fee"]')
                return
            transfer(argv[2].lower(),argv[3],cursor,argv[5])
            return
    if command == "friend":
        if len(argv) != 4:
            print("Error: Incorrect usage of friend.")
            print('Usage: friend userID friendID')
            return
        friend(argv[2].lower(),argv[3].lower(),cursor)
        return
    if command == "balance":
        if len(argv) != 4:
            print("Error: Incorrect usage of balance.")
            print('Usage: balance userID friendID')
            return
        balance(argv[2].lower(),argv[3],cursor)

    if command == "viewprofile":
        if len(argv) != 3:
            print("Error: Incorrect usage of viewprofile.")
            print("Usage: viewprofile userID")
            return
        viewprofile(cursor, argv[2].lower())
        return

    if command == "transactionprivacy":
        if len(argv) != 5:
            print("Error: Incorrect usage of transactionprivacy.")
            print("Usage: transactionPrivacy userID paymentID privacy")
            return
        transactionprivacy(argv[2].lower(),argv[3],argv[4], cursor)
        return

    if command == "setprivacy":
        if len(argv) != 4:
            print("Error: Incorrect usage of setprivacy.")
            print("Usage: setprivacy userID privacy")
            return
        setprivacy(argv[2].lower(),argv[3], cursor)
        return

    if command == "updateprivacy":
        if len(argv) != 5:
            print("Error: Incorrect usage of updateprivacy.")
            print("Usage: updateprivacy userID password privacy")
            return
        updateprivacy(argv[2].lower(),argv[3],argv[4],cursor)
        return

    if command == "unfriend":
        if len(argv) != 4:
            print("Error: Incorrect usage of unfriend.")
            print("Usage: unfriend userID friendID")
            return
        unfriend(argv[2].lower(),argv[3].lower(), cursor)
        return

    if command == "verify":
        if len(argv) != 5:
            print("Error: Incorrect usage of verify.")
            print("Usage: verify userID password SSN")
            return
        verify(argv[2].lower(),argv[3],argv[4],cursor)
        return

    if command == "linkbank":
        if len(argv) != 4:
            print("Error: Incorrect usage of linkbank.")
            print("Usage: linkbank userID bankID")
            return
        linkbank(argv[2].lower(),argv[3],cursor)
        return

    if command == "override":
        if len(argv) != 5:
            print("Error: Incorrect usage of override.")
            print("Usage: override userID password bankID")
            return
        override(argv[2].lower(),argv[3],argv[4],cursor)
        return

    if command == "adduser":
        if len(argv) != 5:
            print("Error: Incorrect usage of adduser.")
            print("Usage: adduser userID password accounttype")
            return
        adduser(argv[2].lower(),argv[3],argv[4],cursor)
        return
    if command == "friendlog":
        if len(argv) == 2:
            print("Usage: friendlog userID friendID [filters]")
            print(f"Possible filters: {filters}")
            return

        if len(argv) == 3:
            print("Usage: friendlog userID friendID [filters]")
            print(f"Possible filters: {filters}")
            return
        userID = argv[2].lower()
        friendID = argv[3].lower()

        if len(argv) == 4:
            friendlog(cursor,userID,friendID)
            return
        above = False
        below = False
        olddate = False
        rangeupper = False
        rangelower = False
        tag = False
        sender = False
        recipient = False
        message = False
        messagecontains = False

        for i in range(4,len(argv),1):
            #makes sure user is inputting valid filters
            if (i%2==0) and argv[i].lower() not in filters:
                print(f"Error: Invalid filter: {argv[i]}.")
                print("Usage: friendlog userID friendID [filters]")
                print(f"Possible filters: {filters}")
                return
            #filters commands are not case sensitive
            if (i%2 ==0):
                argv[i] = argv[i].lower()

            if argv[i] == "-above":
                if below != False:
                    print("Error: You cannot use -above and -below simultaneously. Instead, use -range")
                    return
                if above != False:
                    print("Error: You cannot use -above more than once.")
                    return
                try:
                    above = argv[i+1]
                except IndexError:
                    print("Error: Please enter an amount after -above.")
                    return
                try:
                    above = float(above)
                    if above <0:
                        print("Error: You cannot enter an amount lower than 0.")
                        return
                except ValueError:
                    print("Error: Please enter a numerical amount after -above.")
                    return
                
            if argv[i] == "-below":
                if above != False:
                    print("Error: You cannot use -above and -below simultaneously.")
                    return
                if below != False:
                    print("Error: You cannot use -below more than once.")
                    return
                try:
                    below = argv[i+1]
                except IndexError:
                    print("Error: Please enter an amount after -below.")
                    return
                try:
                    below = float(below)
                except ValueError:
                    print("Error: Please enter a numerical amount after -below.")
                    return
                if below <= 0:
                    print("Error: Amount below must be greater than 0.")
                    return
            if argv[i] == "-range":
                if rangeupper != False:
                    print("Error: You cannot use -range more than once.")
                    return
                try:
                    numberrange = argv[i+1]
                except IndexError:
                    print("Error: Please enter an interval (Example: 1-100) after -range.")
                    return
                if re.match("\\d+-\\d+",numberrange) == None:
                    print("Error: Please enter an interval (Example: 1-100) after -range.")
                    return
                numberrange = numberrange.split("-")                
                rangelower = float(numberrange[0])
                rangeupper = float(numberrange[1])
                
                if rangelower >= rangeupper:
                    print("Error: Invalid interval range. Upper bound of range must exceed the lower bound.")
                    return

            if argv[i] == "-days":
                if olddate != False:
                    print("Error: You cannot use -days more than once.")
                    return
                
                try:
                    days = argv[i+1]
                except IndexError:
                    print("Error: Please enter a number of days after -days.")
                    return
                try:
                    days = int(days)
                except ValueError:
                    print("Error: Please enter an integer amount of days after -days.")
                    return
                if days <= 0:
                    print("Error: Amount of days must be at least one.")
                    return
                
                #get the date from when the user wants 
                olddate = datetime.now() - timedelta(days)
        
            if argv[i] == "-tags":
                if tag != False:
                    print("Error: You cannot use -tags more than once.")
                    return

                try:
                    tag = argv[i+1]
                except IndexError:
                    print("Error: Please enter tag after -tags.")
                    return
                try:
                    tag = tag.lower()
                except SyntaxError:
                    print("Error: Please enter a valid tag. Valid tags are:\n {tags}")
                    return
                if tag.lower() not in tags:
                    print(f"Error: Invalid tag. Valid tags are:\n {tags}")
                    return

            if argv[i] == "-sender":
                if sender != False:
                    print("Error: You cannot use -sender more than once.")
                    return
                try:
                    sender = argv[i+1]
                except IndexError:
                    print("Error: Please enter sender after -sender.")
                    return


            if argv[i] == "-recipient":
                if recipient != False:
                    print("Error: You cannot use -recipient more than once.")
                    return
                try:
                    recipient = argv[i+1]
                except IndexError:
                    print("Error: Please enter recipient after -recipient.")
                    return

            if argv[i] == "-message":
                if message != False:
                    print("Error: You cannot use -message more than once.")
                    return
                try:
                    message = argv[i+1]
                except IndexError:
                    print("Error: Please enter message after -message.")
                    return

            if argv[i] == "-messagecontains":
                if messagecontains != False:
                    print("Error: You cannot use -message more than once.")
                    return
                try:
                    messagecontains = argv[i+1]
                except IndexError:
                    print("Error: Please enter message after -messagecontains.")
                    return
        friendlog(cursor,userID,friendID,below,above,sender,recipient,olddate,message,rangeupper,rangelower,tag,messagecontains)
        return
    if command == "requestlog":
        #usage for -inout: -inout outgoing or -inout incoming
        #-requester userID --> I want to see logs where userID is the REQUESTER
        #-requested userID --> I want to see the logs where userID is the one BEING REQUESTED
        requestlogfilters = ["-above","-below","-range","-days","-tags","-inout","-requester","-requested","-message","-messagecontains","-status"]
        if len(argv) == 2:
            print("Usage: requestlog userID [filters]")
            print(f"Possible filters: {requestlogfilters}")
            return
        userID = argv[2].lower()
        if len(argv) == 3:
            requestlog(cursor,userID)
            return
        above = False
        below = False
        incoming = False
        outgoing = False
        olddate = False
        rangeupper = False
        rangelower = False
        tag = False
        requester = False
        requested = False
        message = False
        messagecontains = False
        status = False

        for i in range(3,len(argv),1):
            if (i%2==1) and argv[i].lower() not in requestlogfilters:
            #makes sure user is inputting valid filters
                print(f"Error: Invalid filter: {argv[i]}.")
                print("Usage: globallog userID [filters]")
                print(f"Possible filters: {requestlogfilters}")
                return
            #filters commands are not case sensitive
            if (i%2 ==1):
                argv[i] = argv[i].lower()
            if argv[i] == "-above":
                if below != False:
                    print("Error: You cannot use -above and -below simultaneously. Instead, use -range")
                    return
                if above != False:
                    print("Error: You cannot use -above more than once.")
                    return
                try:
                    above = argv[i+1]
                except IndexError:
                    print("Error: Please enter an amount after -above.")
                    return
                try:
                    above = float(above)
                    if above <0:
                        print("Error: You cannot enter an amount lower than 0.")
                        return
                except ValueError:
                    print("Error: Please enter a numerical amount after -above.")
                    return
                
            if argv[i] == "-below":
                if above != False:
                    print("Error: You cannot use -above and -below simultaneously.")
                    return
                if below != False:
                    print("Error: You cannot use -below more than once.")
                    return
                try:
                    below = argv[i+1]
                except IndexError:
                    print("Error: Please enter an amount after -below.")
                    return
                try:
                    below = float(below)
                except ValueError:
                    print("Error: Please enter a numerical amount after -below.")
                    return
                if below <= 0:
                    print("Error: Amount below must be greater than 0.")
                    return
            if argv[i] == "-range":
                if rangeupper != False:
                    print("Error: You cannot use -range more than once.")
                    return
                try:
                    numberrange = argv[i+1]
                except IndexError:
                    print("Error: Please enter an interval (Example: 1-100) after -range.")
                    return
                if re.match("\\d+-\\d+",numberrange) == None:
                    print("Error: Please enter an interval (Example: 1-100) after -range.")
                    return
                numberrange = numberrange.split("-")                
                rangelower = float(numberrange[0])
                rangeupper = float(numberrange[1])
                if rangelower >= rangeupper:
                    print("Error: Invalid interval range. Upper bound of range must exceed the lower bound.")
            if argv[i] == "-days":
                if olddate != False:
                    print("Error: You cannot use -days more than once.")
                    return
                
                try:
                    days = argv[i+1]
                except IndexError:
                    print("Error: Please enter a number of days after -days.")
                    return
                try:
                    days = int(days)
                except ValueError:
                    print("Error: Please enter an integer amount of days after -days.")
                    return
                if days <= 0:
                    print("Error: Amount of days must be at least one.")
                    return
                
                #get the date from when the user wants 
                olddate = datetime.now() - timedelta(days)
        
            if argv[i] == "-tags":
                if tag != False:
                    print("Error: You cannot use -tags more than once.")
                    return

                try:
                    tag = argv[i+1]
                except IndexError:
                    print("Error: Please enter tag after -tags.")
                    return
                try:
                    tag = tag.lower()
                except SyntaxError:
                    print("Error: Please enter a valid tag. Valid tags are:\n {tags}")
                    return
                if tag.lower() not in tags:
                    print(f"Error: Invalid tag. Valid tags are:\n {tags}")
                    return

            if argv[i] == "-requester":
                if requester != False:
                    print("Error: You cannot use -requester more than once.")
                    return
                try:
                    requester = argv[i+1]
                except IndexError:
                    print("Error: Please enter requester after -requester.")
                    return

            if argv[i] == "-requested":
                if requested != False:
                    print("Error: You cannot use -requested more than once.")
                    return
                try:
                    requested = argv[i+1]
                except IndexError:
                    print("Error: Please enter the user who received the request after -requested.")
                    return

            if argv[i] == "-message":
                if message != False:
                    print("Error: You cannot use -message more than once.")
                    return
                try:
                    message = argv[i+1]
                except IndexError:
                    print("Error: Please enter message after -message.")
                    return

            if argv[i] == "-messagecontains":
                if messagecontains != False:
                    print("Error: You cannot use -message more than once.")
                    return
                try:
                    messagecontains = argv[i+1]
                except IndexError:
                    print("Error: Please enter message after -messagecontains.")
                    return
            if argv[i] == "-inout":
                if incoming or outgoing:
                    print("Error: You cannot use -inout more than once.")
                    return
                try:
                    inout = argv[i+1].lower()
                except IndexError:
                    print("Error: Please enter either incoming or outgoing after -inout")
                    return
                if inout != "incoming" and inout != "outgoing":
                    print("Error: Please enter either incoming or outgoing after -inout")
                    return
                if inout == "incoming":
                    incoming = True
                elif inout == "outgoing":
                    outgoing = True
            if argv[i] == "-status":
                if status != False:
                    print("Error: You cannot use -status more than once.")
                    return
                try:
                    status = argv[i+1].lower()
                except IndexError:
                    print("Error: Please enter pending, cancelled, accepted, or denied after -status")
                    return
                if status != "pending" and status != "cancelled" and status != "accepted" and status != "denied":
                    print("Error: Please enter pending, cancelled, accepted, or denied after -status")
                    return
                if status == "pending":
                    status = "request"
                elif status == "cancelled":
                    status = "cancelled_request"
                elif status == "accepted":
                    status = "accepted_request"
                elif status == "denied":
                    status = "denied_request"

        requestlog(cursor,userID,below,above,incoming,outgoing,requester,requested,olddate,message,rangeupper,rangelower,tag,messagecontains,status)
        return
    if command == "personallog":
        personallogfilters = ["-above","-below","-range","-days","-tags","-sender","-recipient","-message","-messagecontains","-type"]
        if len(argv) == 2:
            print("Usage: personallog userID [filters]")
            print(f"Possible filters: {personallogfilters}")
            return
        userID = argv[2].lower()
        if len(argv) == 3:
            personallog(cursor,userID)
            return
        above = False
        below = False
        olddate = False
        rangeupper = False
        rangelower = False
        tag = False
        sender = False
        recipient = False
        message = False
        messagecontains = False
        transfersonly = False
        paymentsonly = False

        for i in range(3,len(argv),1):
            if (i%2==1) and argv[i].lower() not in personallogfilters:
            #makes sure user is inputting valid filters
                print(f"Error: Invalid filter: {argv[i]}.")
                print("Usage: personallog userID [filters]")
                print(f"Possible filters: {personallogfilters}")
                return
            #filters commands are not case sensitive
            if (i%2 ==1):
                argv[i] = argv[i].lower()
            if argv[i] == "-above":
                if below != False:
                    print("Error: You cannot use -above and -below simultaneously. Instead, use -range")
                    return
                if above != False:
                    print("Error: You cannot use -above more than once.")
                    return
                try:
                    above = argv[i+1]
                except IndexError:
                    print("Error: Please enter an amount after -above.")
                    return
                try:
                    above = float(above)
                    if above <0:
                        print("Error: You cannot enter an amount lower than 0.")
                        return
                except ValueError:
                    print("Error: Please enter a numerical amount after -above.")
                    return
                
            if argv[i] == "-below":
                if above != False:
                    print("Error: You cannot use -above and -below simultaneously.")
                    return
                if below != False:
                    print("Error: You cannot use -below more than once.")
                    return
                try:
                    below = argv[i+1]
                except IndexError:
                    print("Error: Please enter an amount after -below.")
                    return
                try:
                    below = float(below)
                except ValueError:
                    print("Error: Please enter a numerical amount after -below.")
                    return
                if below <= 0:
                    print("Error: Amount below must be greater than 0.")
                    return
            if argv[i] == "-range":
                if rangeupper != False:
                    print("Error: You cannot use -range more than once.")
                    return
                try:
                    numberrange = argv[i+1]
                except IndexError:
                    print("Error: Please enter an interval (Example: 1-100) after -range.")
                    return
                if re.match("\\d+-\\d+",numberrange) == None:
                    print("Error: Please enter an interval (Example: 1-100) after -range.")
                    return
                numberrange = numberrange.split("-")                
                rangelower = float(numberrange[0])
                rangeupper = float(numberrange[1])
                if rangelower >= rangeupper:
                    print("Error: Invalid interval range. Upper bound of range must exceed the lower bound.")
            if argv[i] == "-days":
                if olddate != False:
                    print("Error: You cannot use -days more than once.")
                    return
                
                try:
                    days = argv[i+1]
                except IndexError:
                    print("Error: Please enter a number of days after -days.")
                    return
                try:
                    days = int(days)
                except ValueError:
                    print("Error: Please enter an integer amount of days after -days.")
                    return
                if days <= 0:
                    print("Error: Amount of days must be at least one.")
                    return
                
                #get the date from when the user wants 
                olddate = datetime.now() - timedelta(days)
        
            if argv[i] == "-tags":
                if tag != False:
                    print("Error: You cannot use -tags more than once.")
                    return

                try:
                    tag = argv[i+1]
                except IndexError:
                    print("Error: Please enter tag after -tags.")
                    return
                try:
                    tag = tag.lower()
                except SyntaxError:
                    print("Error: Please enter a valid tag. Valid tags are:\n {tags}")
                    return
                if tag.lower() not in tags:
                    print(f"Error: Invalid tag. Valid tags are:\n {tags}")
                    return

            if argv[i] == "-sender":
                if sender != False:
                    print("Error: You cannot use -sender more than once.")
                    return
                try:
                    sender = argv[i+1]
                except IndexError:
                    print("Error: Please enter sender after -sender.")
                    return


            if argv[i] == "-recipient":
                if recipient != False:
                    print("Error: You cannot use -recipient more than once.")
                    return
                try:
                    recipient = argv[i+1]
                except IndexError:
                    print("Error: Please enter recipient after -recipient.")
                    return

            if argv[i] == "-message":
                if message != False:
                    print("Error: You cannot use -message more than once.")
                    return
                try:
                    message = argv[i+1]
                except IndexError:
                    print("Error: Please enter message after -message.")
                    return

            if argv[i] == "-messagecontains":
                if messagecontains != False:
                    print("Error: You cannot use -message more than once.")
                    return
                try:
                    messagecontains = argv[i+1]
                except IndexError:
                    print("Error: Please enter message after -messagecontains.")
                    return

            if argv[i] == "-type":
                if paymentsonly:
                    print("Error: You cannot use -type more than once.")
                    return
                if transfersonly:
                    print("Error: You cannot use -type more than once.")
                    return
                try:
                    type = argv[i+1].lower()
                except IndexError:
                    print("Error: Please enter transfers or payments after -type")
                    return
                if type != "transfers" and type != "payments":
                    print("Error: Please enter transfers or payments after -type")
                    return
                if type == "transfers":
                    transfersonly = True
                elif type == "payments":
                    paymentsonly = True
        personallog(cursor,userID,below,above,sender,recipient,olddate,message,rangeupper,rangelower,tag,messagecontains,transfersonly,paymentsonly)

        return

