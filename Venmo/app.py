import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from webhelpers import apology, login_required, lookup, usd
from datetime import datetime, timedelta
from helpers import getbalance,getfees,friendgetter,isVerified,numrequests, personallogpreview, friendcheck, validateusernoprint, limitenforcernoprint,verifiedtime, paynoprint,requestnoprint,friendandgloballogpreview

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def fetch(fetchone):
    return str(''.join(fetchone))

def get_db_connection():
    conn = sqlite3.connect('venmo.db')
    #conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def login():
    """Log user in"""
    try:
        if session["user_id"] != None:
            return redirect("/home")
    except KeyError:
        counter1234567890=0
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Query database for username
        conn = get_db_connection()
        cursor = conn.cursor()
        if not (request.form.get("username")):
            return render_template("login.html",errorcode = "Please enter a username.")
        if not (request.form.get("password")):
            return render_template("login.html",errorcode = "Please enter a password.")

        cursor.execute('''SELECT password FROM users WHERE username = ?''',(request.form.get("username"),))
        #checks if user exists
        correctpassword = cursor.fetchone()
        conn.close()
        if correctpassword == None:
            return render_template("login.html",errorcode = "An account with this username does not exist. Please double-check your username.")
        correctpassword = str(''.join(correctpassword))

        #password is correct
        if request.form.get("password") != correctpassword:
            return render_template("login.html",errorcode = "Sorry, your password was incorrect. Please double-check your password.")

        # Remember which user has logged in
        session["user_id"] = request.form.get("username")

        # Redirect user to home page
        return redirect("/home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html",errorcode = '')

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        errorcode = []
        # Query database for username
        conn = get_db_connection()
        cursor = conn.cursor()
        
        username = request.form.get("username")
        password = request.form.get("password")
        accounttype = request.form.get("accounttype")

        # Ensure username was submitted
        if not username:
            errorcode.append("• You must enter a username.")

        # Ensure password was submitted and making sure the password is good
        if not password:
            errorcode.append("• You must enter a password.")
        
        #Ensure account type was submitted
        if not accounttype:
            errorcode.append("• You must enter an account type.")

        
        # Check if username is already in database
        cursor.execute(''' SELECT password FROM users WHERE username = ? ''', (username,))
        if cursor.fetchone():
            errorcode.append("• An account with this username already exists.")

        if str(request.form.get("confirmation")) != str(password):
            errorcode.append("• Password and confirmation do not match.")
        if len(errorcode) !=0:
            return render_template("register.html",errorcode=errorcode,len_errorcode=len(errorcode))
        
        date = str(datetime.now())
        date = date[0:10]

        cursor.execute(''' INSERT INTO users (username, friends, balance, accounttype, password, creationDate) 
        VALUES (?,?,?,?,?,?) ''',
        (username, "*", 0.0, accounttype, password, date))
        conn.commit()
        conn.close()

        return redirect("/")

    else:
        return render_template("register.html",errorcode = [],len_errorcode=0)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        counter=0
    else:
        userID = session["user_id"]
        conn = get_db_connection()
        cursor = conn.cursor()
        #fetching profile information
        balance = getbalance(userID, cursor)
        fees = getfees(userID, cursor)
        friends = friendgetter(userID, cursor)
        numFriends = len(friends)
        numRequests = numrequests(userID,cursor)
        if (numFriends == 1) and friends == ["*"]:
            numFriends = 0
        verified = isVerified(userID, cursor)
        cursor.execute(''' SELECT creationDate FROM users WHERE username=?''', (userID,))
        date = fetch(cursor.fetchone())

        # Log Preview #
        #0 = senderID, 1 = recipientID, 2 = amount, 3 = date 4= message 5= paymentID
        #6 = privacy 7 = tag 8 = senderBalance 9 = recipientBalance 10 = status
        personallog = personallogpreview(userID,cursor)
        friendlog,globallog = friendandgloballogpreview(userID,cursor)

        conn.close()
        return render_template('home.html',userID=userID,balance=balance,fees=fees,numFriends=numFriends,verified=verified,date=date,numrequests=numRequests,personallog=personallog,friendlog=friendlog)

@app.route("/pay", methods=["GET", "POST"])
@login_required
def pay():
    if request.method == "POST":
        senderID = session["user_id"]
        tags = ["food", "groceries", "rent", "utilities", "sports", "fun", "transportation", "drinks", "business", "tickets", "gift", "gas"]
        transactiontype = request.form.get("payorrequest")
        recipientID = request.form.get("username")
        amount = request.form.get("amount")
        message = request.form.get("message")
        tag = request.form.get("tag")
        privacy = request.form.get("privacy")
        # Making sure the user actually typed in valid values #
        if not transactiontype:
            return render_template('pay.html',errormessage="Please enter a transaction type.")
        if not recipientID:
            return render_template('pay.html',errormessage="Please enter a recipient.")
        if not amount:
            return render_template('pay.html',errormessage="Please enter a payment amount.")
        try:
            amount = float(amount)
        except ValueError:
            return render_template('pay.html',errormessage="Please enter a numerical payment amount.")
        if amount <= 0:
            return render_template('pay.html',errormessage="You cannot pay or request less than or equal to 0 dollars.")
        if not message:
            return render_template('pay.html',errormessage="Please enter a message.")
        if (tag) and (tag.lower() not in tags):
            return render_template('pay.html',errormessage="Please enter a valid tag.",recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy)
        if transactiontype == "Pay" and privacy not in ["Private","Friends Only","Public"]:
            return render_template('pay.html',errormessage="Please enter a valid privacy.",recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy)

        # checking important stuff #
        conn = get_db_connection()
        cursor = conn.cursor()

        if senderID == recipientID:
            return render_template('pay.html',errormessage=f"You cannot {transactiontype.lower()} yourself!",recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy)

        if not validateusernoprint(recipientID,cursor):
            return render_template('pay.html',errormessage=f"User '{recipientID}' does not exist.",recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy)

        if not friendcheck(senderID,recipientID,cursor):
            return render_template('pay.html',errormessage=f"You are not friends with {recipientID}.",recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy)

        withinlimit,limiterror = limitenforcernoprint(senderID,transactiontype.lower(),amount,cursor)
        if not withinlimit:
            return render_template('pay.html',errormessage=limiterror,recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy)

        if not verifiedtime(senderID,120,cursor):
            return render_template('pay.html',errormessage=f"Error: To complete a payment or request you must verify your account in the past 120 days.",recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy)
        if transactiontype == "Pay":
            paymentworked,paymenterror = paynoprint(senderID,recipientID,amount,message,cursor,privacy,tag)
            if not paymentworked:
                return render_template('pay.html',errormessage=paymenterror,recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy)
        elif transactiontype == "Request":
            requestnoprint(senderID,recipientID,amount,message,cursor,tag)

        conn.commit()
        conn.close()

        return render_template('success.html',transactiontype=transactiontype,recipientID=recipientID,amount=amount)
    else:
        return render_template('pay.html',errormessage="")
