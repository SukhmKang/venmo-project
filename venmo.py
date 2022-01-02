import sqlite3
import sys
from datetime import datetime

tags = ["food", "groceries", "rent", "utilities", "sports", "fun", "transportation", "drinks", "business", "tickets", "gift", "gas"]
db = sqlite3.connect('venmo.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS paymentLog (senderID TEXT, recipientID TEXT, amount FLOAT, status TEXT, date DATETIME, message TEXT, paymentID TEXT, privacy TEXT, tag TEXT, senderBalance FLOAT, recipientBalance FLOAT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, friends TEXT, balance FLOAT DEFAULT 0.0, accounttype TEXT, bank TEXT DEFAULT None, privacy TEXT DEFAULT None)''')

if len(sys.argv) == 1:
    print("Please enter a command.")
else:
    if sys.argv[1] == "pay":
        if len(sys.argv) == 6:
            pay(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
        elif len(sys.argv) == 7:
            pay(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
        elif len(sys.argv) == 8:
            pay(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7])
    if sys.argv[1] == "request":
        request()
    if sys.argv[1] == "unrequest":
        unrequest()
    if sys.argv[1] == "deposit":
        deposit()
    if sys.argv[1] == "transfer":
        transfer()
    if sys.argv[1] == "friend":
        friend()
    if sys.argv[1] == "adduser":
        adduser()
    if sys.argv[1] == "globallog":
        globallog()
    if sys.argv[1] == "friendlog":
        friendlog()
    if sys.argv[1] == "personallog":
        personallog()
    if sys.argv[1] == "transactionslog":
        transactionslog()
    if sys.argv[1] == "requestlog":
        requestlog()
    if sys.argv[1] == "viewprofile":
        viewprofile()



db.commit()
db.close()

def pay(senderID,recipientID,amount,message,tag=None,privacy=None):
    cursor.execute(''' SELECT username FROM users WHERE username=?''', (senderID))
    if cursor.fetchone() == None:
        print("Error: Sender not in system.")
        return
    cursor.execute(''' SELECT username FROM users WHERE username =?''', (recipientID))
    if cursor.fetchone() == None:
        print("Error: Recipient not in system.")
        return
    #error checking: need to check if amount is a numerical value or not
    #not much to check for the message
    senderprivacy = cursor.execute(''' SELECT privacy FROM users WHERE username=? ''', (senderID))
    recipientprivacy = cursor.execute(''' SELECT privacy FROM users WHERE username=? ''', (recipientID))
    if senderprivacy or recipientprivacy == "Private":
        privacy = "Private"
    elif senderprivacy or recipientprivacy == "Friends Only":
        privacy = "Friends Only"
    elif senderprivacy == "Public" and recipientprivacy == "Public":
        privacy = "Public"
    else:
        print("Error: Neither user has a default privacy setting and a privacy setting was not manually inputted.")
        return
    
    if tag != None and tag.lower().strip() not in tags:
        print("Error: Invalid tag.")
        return

    if float(amount) > float(cursor.execute(''' SELECT balance FROM users WHERE username=? ''', (senderID))):
        print("Error: Sender does not have enough money in account.")
        return

    #need to develop hashing function to generate payment ID
    paymentID = hash(str(senderID)+str(recipientID)+str(message)+str(datetime.now()))
    senderBalance = float(cursor.execute(''' SELECT balance FROM users WHERE username=? ''', (senderID))) - float(amount)
    recipientBalance = float(cursor.execute(''' SELECT balance FROM users WHERE username=? ''', (recipientID))) - float(amount)
    cursor.execute(''' INSERT INTO paymentLog (senderID, recipientID, amount, status, date, message, paymentID, privacy, tag, senderBalance, recipientBalance)
    VALUES (?,?,?,?,?,?,?,?,?,?,?) '''
    (senderID,recipientID,amount,"_payment",datetime.now(),message,paymentID,privacy,tag,senderBalance,recipientBalance))
def request(userID, friendID,amount,message,tag=None):

def unrequest(paymentID):

def deposit(userID, amount):
def transfer(userID, amount):
def friend(userID, friendID):
def adduser(userID):
def globallog(argv):
def friendlog(argv):
def personallog(argv):
def transactionslog(argv):
def requestlog(argv):
def viewprofile(userID):
        