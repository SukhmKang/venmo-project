import sqlite3
import sys
from helpers import pay, request, unrequest, deposit, transfer, friend, adduser, globallog, friendlog, personallog, transactionslog, requestlog, viewprofile

tags = ["food", "groceries", "rent", "utilities", "sports", "fun", "transportation", "drinks", "business", "tickets", "gift", "gas"]
db = sqlite3.connect('venmo.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS paymentLog (senderID TEXT, recipientID TEXT, amount FLOAT, status TEXT, date DATETIME, message TEXT, paymentID TEXT, privacy TEXT, tag TEXT, senderBalance FLOAT, recipientBalance FLOAT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, friends TEXT DEFAULT "*", balance FLOAT DEFAULT 0.0, accounttype TEXT, bank TEXT DEFAULT None, privacy TEXT DEFAULT None)''')

def init(argv,cursor):
    if len(argv) == 1:
        print("Please enter a command.")
        return
    else:
        if argv[1] == "pay":
            if len(argv) == 6:
                pay(argv[2],argv[3],argv[4],argv[5],cursor)
            elif len(argv) == 7:
                pay(argv[2],argv[3],argv[4],argv[5],cursor,argv[6])
            elif len(argv) == 8:
                pay(argv[2],argv[3],argv[4],argv[5],cursor,argv[6],argv[7])
            else:
                print("Usage: python3 venmo.py pay senderID recipientID amount message [tag] [privacy]")
            return
        if argv[1] == "request":
            request()
            return
        if argv[1] == "unrequest":
            unrequest()
            return
        if argv[1] == "deposit":
            deposit()
            return
        if argv[1] == "transfer":
            transfer()
            return
        if argv[1] == "friend":
            if len(argv) == 4:
                friend(argv[2], argv[3], cursor)
            return
        if argv[1] == "adduser":
            if len(argv) == 4:
                adduser(argv[2], argv[3],cursor)
            return
        if argv[1] == "globallog":
            globallog()
            return
        if argv[1] == "friendlog":
            friendlog()
            return
        if argv[1] == "personallog":
            personallog()
            return
        if argv[1] == "transactionslog":
            transactionslog()
            return
        if argv[1] == "requestlog":
            requestlog()
            return
        if argv[1] == "viewprofile":
            viewprofile()
            return
        print("Please enter a valid command.")

init(sys.argv,cursor)

db.commit()
db.close()
