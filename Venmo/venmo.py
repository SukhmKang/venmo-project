import sqlite3
import sys
from datetime import datetime
from helpers import inputvalidater,getprivacy

#Initializes database
db = sqlite3.connect('venmo.db')
#creates cursor object to pass into inputvalidater
cursor = db.cursor()
#Sets up tables
cursor.execute('''CREATE TABLE IF NOT EXISTS paymentLog (senderID TEXT, recipientID TEXT, amount FLOAT, status TEXT, date DATETIME, message TEXT, paymentID TEXT, privacy TEXT, tag TEXT, senderBalance FLOAT, recipientBalance FLOAT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, friends TEXT DEFAULT "*", balance FLOAT DEFAULT 0.0, accounttype TEXT, bank TEXT DEFAULT "*", privacy TEXT DEFAULT "*", verification DATETIME DEFAULT "0001-01-01 00:00:00.0", ssn TEXT DEFAULT "*", fees FLOAT DEFAULT 0.0, creationDate TEXT, friendReqs TEXT DEFAULT "*") ''')

#opens command file in read mode
with open ("commands.txt","r") as commands:
    #loops through each line of commands
    for line in commands:
        stripped_line = line.strip()
        #turns each line of commands into a list
        stripped_line = stripped_line.split(",")
        #passes command into input validater
        #inputvalidater(stripped_line,cursor)

#accepts command line input here
inputvalidater(sys.argv,cursor)

db.commit()
db.close()
