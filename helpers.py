from datetime import datetime
tags = ["food", "groceries", "rent", "utilities", "sports", "fun", "transportation", "drinks", "business", "tickets", "gift", "gas"]

def pay(senderID,recipientID,amount,message,cursor,tag=None,privacy=None):
    cursor.execute(''' SELECT username FROM users WHERE username=?''', (senderID,))
    if cursor.fetchone() == None:
        print("Error: Sender not in system.")
        return
    cursor.execute(''' SELECT username FROM users WHERE username =?''', (recipientID,))
    if cursor.fetchone() == None:
        print("Error: Recipient not in system.")
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

    #not much to check for the message
    cursor.execute(''' SELECT friends FROM users WHERE username=?''',(senderID,))
    senderFriends = ''.join(cursor.fetchone())


    if recipientID not in senderFriends:
        print("Error: You are not friends with " + recipientID + ".")
        return

    cursor.execute(''' SELECT privacy FROM users WHERE username=? ''', (senderID,))
    try:
        senderprivacy = ''.join(cursor.fetchone())
    except TypeError:
        print("Sender does not have default privacy setting...checking if user specified privacy in payment")
        senderprivacy = None
    
    cursor.execute(''' SELECT privacy FROM users WHERE username=? ''', (recipientID,))
    try:
        recipientprivacy = ''.join(cursor.fetchone())
    except TypeError:
        print("Recipient does not have default privacy setting...checking if user specified privacy in payment")
        recipientprivacy = None

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

    if privacy != "Private" and privacy != "Friends Only" and privacy != "Public":
        print("Error: Privacy input must be 'Privacy' or 'Friends Only' or 'Public'.")
        return

    if tag != None and tag.lower().strip() not in tags:
        print("Error: Invalid tag.")
        return
    
    cursor.execute(''' SELECT balance FROM users WHERE username=? ''', (senderID,))
    senderBalance = str(cursor.fetchone()).replace("(","").replace(")","").replace(",","")
    senderBalance = float(senderBalance)

    cursor.execute(''' SELECT balance FROM users WHERE username=? ''', (recipientID,))
    recipientBalance = str(cursor.fetchone()).replace("(","").replace(")","").replace(",","")
    recipientBalance = float(recipientBalance)

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

def request(userID, friendID,amount,message,tag=None):
    return

def unrequest(paymentID):
    return

def deposit(userID, amount):
    

    return

def transfer(userID, amount, type, cursor):
    return

def friend(userID, friendID, cursor):
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

def adduser(userID, accountType,cursor):
    if str(accountType.lower()) != "personal" and str(accountType.lower()) != "business":
        print("Error: Invalid account type.")
        return
    cursor.execute(''' SELECT username FROM users WHERE username LIKE ?''', (userID,))
    if cursor.fetchone():
        print("Error: Account with that username already exists.")
        return
    cursor.execute(''' INSERT INTO users (username, friends, balance, accounttype, bank, privacy) 
    VALUES (?,?,?,?,?,?) ''',
    (userID, "*", 0.0, accountType, None, None))
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


