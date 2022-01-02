import sqlite3
import sys

tags = ["food", "groceries", "rent", "utilities", "sports", "fun", "transportation", "drinks", "business", "tickets", "gift", "gas"]
db = sqlite3.connect('venmo.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS paymentLog (senderID TEXT, recipientID TEXT, amount FLOAT, status TEXT, date DATETIME, message TEXT, paymentID TEXT, privacy TEXT, tag TEXT, senderBalance FLOAT, recipientBalance FLOAT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, friends TEXT, balance FLOAT, accounttype TEXT)''')

if len(sys.argv) == 1:
    print("Please enter a command.")
else:
    if sys.argv[1] == "pay":
        if len(sys.argv) == 6:
            pay(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
        elif len(sys.argv) == 7:
            pay(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
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

def pay(senderID,recipientID,amount,message,tag=None):


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
        