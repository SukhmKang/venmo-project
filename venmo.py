import sqlite3
import sys
from datetime import datetime
from helpers import pay, request, unrequest, deposit, transfer, friend, adduser, globallog, friendlog, personallog, transactionslog, requestlog, viewprofile, linkbank, override, verify, setprivacy

tags = ["food", "groceries", "rent", "utilities", "sports", "fun", "transportation", "drinks", "business", "tickets", "gift", "gas"]
db = sqlite3.connect('venmo.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS paymentLog (senderID TEXT, recipientID TEXT, amount FLOAT, status TEXT, date DATETIME, message TEXT, paymentID TEXT, privacy TEXT, tag TEXT, senderBalance FLOAT, recipientBalance FLOAT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, friends TEXT DEFAULT "*", balance FLOAT DEFAULT 0.0, accounttype TEXT, bank TEXT DEFAULT "*", privacy TEXT DEFAULT "*", verification DATETIME DEFAULT "0001-01-01 00:00:00.0", ssn TEXT DEFAULT "*") ''')

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
            #request userID friendID amount message [tag]
            if len(argv) == 6:
                request(argv[2],argv[3],argv[4],argv[5],cursor)
            if len(argv) == 7:
                request(argv[2],argv[3],argv[4],argv[5],cursor,argv[6])
            return
        if argv[1] == "unrequest":
            unrequest()
            return
        if argv[1] == "deposit":
            #deposit userID amount
            if len(argv) == 4:
                deposit(argv[2],argv[3],cursor)
            return
        if argv[1] == "transfer":
            transfer()
            return
        if argv[1] == "friend":
            if len(argv) == 4:
                friend(argv[2], argv[3], cursor)
            return
        if argv[1] == "adduser":
            #adduser userID password accounttype
            if len(argv) == 5:
                adduser(argv[2],argv[3],argv[4],cursor)
            return
        if argv[1] == "linkBank":
            #linkBank userID bankID
            if len(argv) == 4:
                linkbank(argv[2],argv[3],cursor)
            return
        if argv[1] == "override":
            #override userID password bankID
            if len(argv) == 5:
                override(argv[2],argv[3],argv[4],cursor)
            return
        if argv[1] == "verify":
            #verify userID password SSN
            if len(argv) == 5:
                verify(argv[2],argv[3],argv[4],cursor)
                return
        if argv[1] == "setPrivacy":
            setprivacy()
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
