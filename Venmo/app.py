import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from webhelpers import apology, login_required, usd
from datetime import datetime, timedelta
from helpers import acceptFriendReq, denyFriendReq, getbalance,getfees,friendgetter,isVerified,numrequests, personallogpreview, friendcheck, validateusernoprint, limitenforcernoprint,verifiedtime, paynoprint,requestnoprint,friendandgloballogpreview, transferlogpreview, requestlogpreview,requestgetter, friendReqgetter, acceptrequestnoprint, denyrequestnoprint,allusersexceptfriends,getbank,transfernoprint,friendreqnoprint, friendReq,lastverified,getprivacy,verifynoprint,linkbanknoprint,updateprivacynoprint,changepasswordnoprint,get_log,depositnoprint,fixdate

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
        log_type = request.form.get('logbutton')
        return render_template('logs.html',log_selection=log_type)
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
        bankID = getbank(userID,cursor)
        hasbank = bankID != '*'
        if hasbank:
            bankID = "*****" + bankID[5:]
        # Log Preview #
        #0 = senderID, 1 = recipientID, 2 = amount, 3 = date 4= message 5= paymentID
        #6 = privacy 7 = tag 8 = senderBalance 9 = recipientBalance 10 = status
        personallog = personallogpreview(userID,cursor)
        friend_log,global_log = friendandgloballogpreview(userID,cursor)
        transferlog = transferlogpreview(userID, cursor)
        requestlog = requestlogpreview(userID, cursor)
        conn.close()
        return render_template('home.html',userID=userID,balance=balance,fees=fees,numFriends=numFriends,verified=verified,date=date,numrequests=numRequests,personallog=personallog,friendlog=friend_log, globallog=global_log, transferlog=transferlog, requestlog=requestlog, hasbank=hasbank,bankID=bankID)

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
            return render_template('pay.html',errormessage="Error: Please enter a transaction type.",redirect=False)
        if not recipientID:
            return render_template('pay.html',errormessage="Error: Please enter a recipient.",redirect=False)
        if not amount:
            return render_template('pay.html',errormessage="Error: Please enter a payment amount.",redirect=False)
        try:
            amount = float(amount)
        except ValueError:
            return render_template('pay.html',errormessage="Error: Please enter a numerical payment amount.",recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy,redirect=False)
        if amount <= 0:
            return render_template('pay.html',errormessage="Error: You cannot pay or request less than or equal to 0 dollars.",recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy,redirect=False)
        if not message:
            return render_template('pay.html',errormessage="Error: Please enter a message.",recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy,redirect=False)
        if (tag) and (tag.lower() not in tags):
            return render_template('pay.html',errormessage="Error: Please enter a valid tag.",recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy,redirect=False)
        if transactiontype == "Pay" and privacy not in ["Private","Friends Only","Public"]:
            return render_template('pay.html',errormessage="Error: Please enter a valid privacy.",recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy,redirect=False)

        # checking important stuff #
        conn = get_db_connection()
        cursor = conn.cursor()

        if senderID == recipientID:
            return render_template('pay.html',errormessage=f"Error: You cannot {transactiontype.lower()} yourself!",recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy,redirect=False)

        if not validateusernoprint(recipientID,cursor):
            return render_template('pay.html',errormessage=f"Error: User '{recipientID}' does not exist.",recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy,redirect=False)

        if not friendcheck(senderID,recipientID,cursor):
            return render_template('pay.html',errormessage=f"Error: You are not friends with {recipientID}.",recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy,redirect=False)

        withinlimit,limiterror = limitenforcernoprint(senderID,transactiontype.lower(),amount,cursor)
        if not withinlimit:
            return render_template('pay.html',errormessage=limiterror,recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy,redirect=False)

        if not verifiedtime(senderID,120,cursor):
            return render_template('pay.html',errormessage=f"Error: To complete a payment or request you must verify your account in the past 120 days.",recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy,redirect=False)
        if transactiontype == "Pay":
            paymentworked,paymenterror = paynoprint(senderID,recipientID,amount,message,cursor,privacy,tag)
            if not paymentworked:
                return render_template('pay.html',errormessage=paymenterror,recipientID=recipientID,transactiontype=transactiontype,amount=amount,message=message,tag=tag,privacy=privacy,redirect=False)
        elif transactiontype == "Request":
            requestnoprint(senderID,recipientID,amount,message,cursor,tag)

        conn.commit()
        conn.close()
        return render_template('pay.html',errormessage=f"Success! You sent @{recipientID} ${amount}!")
        #return render_template('success.html',transactiontype=transactiontype,recipientID=recipientID,amount=amount)
    else:
        return render_template('pay.html',errormessage="",redirect=False)

@app.route("/requests", methods=["GET", "POST"])
@login_required
def requests():
    if request.method == "POST":
        userID = session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor()

        requestsubmission = request.form['submitbutton']
        if requestsubmission[0:7] == "accept-":
            requestID=requestsubmission[7:]
            acceptsuccess,error = acceptrequestnoprint(userID,requestID,cursor)
            if acceptsuccess:
                message = f'Successfully accepted payment {requestID}.'
            else:
                message = '_' + error
        elif requestsubmission[0:5] == "deny-":
            requestID=requestsubmission[5:]
            denyrequestnoprint(userID,requestID,cursor)
            message = f'Denied payment {requestID}.'
        if requestsubmission[0:13] == "acceptfriend-":
            friendID=requestsubmission[13:]
            acceptFriendReq(userID,friendID,cursor)
            message = f'Successfully added {friendID} as a friend.'
        elif requestsubmission[0:11] == "denyfriend-":
            friendID=requestsubmission[11:]
            denyFriendReq(userID,friendID,cursor)
            message = f'Denied friend request from {friendID}.'
        paymentrequests = requestgetter(userID,cursor)
        friendrequests = friendReqgetter(userID, cursor)
        if friendrequests == ['*']:
            friendrequests = []
        conn.commit()
        conn.close()

        return render_template('requests.html',paymentrequests=paymentrequests,friendrequests=friendrequests,message=message)
    else:
        userID = session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        paymentrequests = requestgetter(userID,cursor)
        friendrequests = friendReqgetter(userID,cursor)
        if friendrequests == ['*']:
            friendrequests = []
        conn.close()
        return render_template('requests.html',paymentrequests=paymentrequests,friendrequests=friendrequests, message='')

@app.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    if request.method == "POST":
        conn = get_db_connection()
        cursor = conn.cursor()
        error = ''
        userID = session['user_id']
        balance = getbalance(userID,cursor)
        #Amount to transfer
        amount = request.form.get('amount')
        amount = float(amount)
        #seeing whether they clicked default or other bank
        radio = request.form.get("bank")
        #transfer type
        transfertype = request.form.get("transfertype")
        #(If doesn't have a bank) get the bank ID they want to transfer to
        newbank_hasnobank = request.form.get("newbank_hasnobank")
        if newbank_hasnobank == '':
            hasbank = True
            if radio == "otherbank":
                #if clicked other bank, get the new bank ID
                bankID = request.form.get("newbank")
                makedefault = request.form.get("makedefault")
                makedefault = makedefault == "makedefault"
            else:
                #if clicked default, store the default bankID
                makedefault = False
                bankID = getbank(userID,cursor)
            transfer_worked,error=transfernoprint(userID,amount,cursor,transfertype,bankID,makedefault)
        else:
            makedefault = request.form.get('makedefault_hasnobank')
            makedefault = makedefault == "makedefault_hasnobank"
            hasbank = makedefault
            bankID = request.form.get('newbank_hasnobank')
            transfer_worked,error=transfernoprint(userID,amount,cursor,transfertype,bankID,makedefault)
        conn.commit()
        conn.close()
        return render_template('transfer.html',userID=userID,bankID=bankID,balance=balance,hasbank=hasbank,transfer_worked=transfer_worked,message=error)
    else:
        userID = session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        bankID = getbank(userID,cursor)
        hasbank = bankID != '*'
        balance = getbalance(userID,cursor)
        if hasbank:
            bankID = "*****" + bankID[5:]
        conn.close()
        return render_template('transfer.html',userID=userID,bankID=bankID,hasbank=hasbank,balance=balance,message='')

@app.route("/social", methods=["GET", "POST"])
@login_required
def social():
    if request.method == "POST":
        userID = session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        requestsubmission = request.form['submitbutton']
        if requestsubmission[0:13] == "acceptfriend-":
            friendID=requestsubmission[13:]
            acceptFriendReq(userID,friendID,cursor)
            message = f'Successfully added {friendID} as a friend.'
        elif requestsubmission[0:11] == "denyfriend-":
            friendID=requestsubmission[11:]
            denyFriendReq(userID,friendID,cursor)
            message = f'Denied friend request from {friendID}.'
        elif requestsubmission[0:4] == "pay-":
            recipientID=requestsubmission[4:]
            return render_template('pay.html',errormessage='',recipientID=recipientID,transactiontype="Pay",privacy="No Selection",redirect=True)
        elif requestsubmission[0:8] == "request-":
            recipientID=requestsubmission[8:]
            return render_template('pay.html',errormessage='',recipientID=recipientID,transactiontype="Request",privacy="No Selection",redirect=True)
        elif requestsubmission == "friendrequest":
            friendID = request.form.get("username")
            friendreqworked,error = friendReq(userID,friendID,cursor)
            allusers = allusersexceptfriends(userID,cursor)
            friendrequests = friendReqgetter(userID, cursor)
            if friendrequests == ['*']:
                friendrequests = []
            friends = friendgetter(userID, cursor)
            if friends == ['*']:
                friends = []
            conn.commit()
            conn.close()
            return render_template('social.html',friendrequests=friendrequests,message=error,friends=friends,userbase=allusers)
        allusers = allusersexceptfriends(userID,cursor)
        friendrequests = friendReqgetter(userID, cursor)
        if friendrequests == ['*']:
            friendrequests = []
        friends = friendgetter(userID, cursor)
        if friends == ['*']:
            friends = []

        conn.commit()
        conn.close()
        return render_template('social.html',friendrequests=friendrequests,message=message,friends=friends,userbase=allusers)
    else:
        userID = session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        friendrequests = friendReqgetter(userID,cursor)
        if friendrequests == ['*']:
            friendrequests = []
        friends = friendgetter(userID, cursor)
        if friends == ['*']:
            friends = []
        allusers = allusersexceptfriends(userID,cursor)

        conn.close()

        return render_template('social.html',friendrequests=friendrequests,message='',friends=friends,userbase=allusers)

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        userID=session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        ### Getting form submission
        currprivacy = getprivacy(userID,cursor)
        ### returns empty string if they didn't fill out the category
        verify = request.form.get('verifyaccount')
        changebank = request.form.get('changebank')
        newprivacy = request.form.get('privacy')
        if newprivacy == None:
            newprivacy = '*'
        currentpassword = request.form.get('currentpassword')
        newpassword = request.form.get('newpassword')
        confirmnewpassword = request.form.get('confirmnewpassword')
        updated_verify = verify != ''
        changed_bank = changebank != ''
        changed_privacy = newprivacy != currprivacy
        changed_password = (currentpassword != '' and newpassword != '' and confirmnewpassword != '')
        messages = {}
        # None = wasn't inputted, False = failed, True = succeeded
        verification_worked = None
        linkbank_worked = None
        updatepriv_worked = None
        changepass_worked = None
        if updated_verify:
            verification_worked, verification_error = verifynoprint(userID,verify,cursor)
            messages['verified'] = verification_error
        if changed_bank:
            linkbank_worked, bank_error = linkbanknoprint(userID,changebank,cursor)
            messages['bank'] = bank_error
        if changed_privacy:
            updatepriv_worked, priv_error = updateprivacynoprint(userID,newprivacy,cursor)
            messages['privacy'] = priv_error
        if changed_password:
            changepass_worked, changepass_error = changepasswordnoprint(userID,currentpassword,newpassword,confirmnewpassword,cursor)
            messages['password'] = changepass_error
        bankID = getbank(userID,cursor)
        hasbank = bankID != '*'
        verified = isVerified(userID, cursor)
        privacy = getprivacy(userID,cursor)
        if verified:
            last_verified = lastverified(userID,cursor)
        else:
            last_verified = 1000000000000 #idk what to make it

        conn.commit()
        conn.close()
        return render_template('settings.html',userID=userID,hasbank=hasbank,last_verified=last_verified,verified=verified,bankID=bankID,privacy=privacy,verification_worked=verification_worked,linkbank_worked=linkbank_worked,updatepriv_worked=updatepriv_worked,changepass_worked=changepass_worked,messages=messages)

    else:
        userID = session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        bankID = getbank(userID,cursor)
        hasbank = bankID != '*'
        verified = isVerified(userID, cursor)
        privacy = getprivacy(userID,cursor)
        if verified:
            last_verified = lastverified(userID,cursor)
        else:
            last_verified = 1000000000000 #idk what to make it
        conn.close()
        return render_template("settings.html",userID=userID,hasbank=hasbank,last_verified=last_verified,verified=verified,bankID=bankID,privacy=privacy,messages=[])

@app.route("/logs", methods=["GET", "POST"])
@login_required
def logs():
    if request.method == "POST":
        userID = session['user_id']
        filters = {}
        #Type of log (personal, friend, global, request, transfer)
        for elem in ['logtype','sender','recipient','below','above','lower','upper','days','fromdate','todate','message','messagecontains','tag','transfertype','status']:
            filters[elem] = request.form.get(elem)
        filtered = {}
        for elem in ['logtype','sender','recipient','below','above','lower','upper','days','fromdate','todate','message','messagecontains','tag']:
            filtered[elem] = filters[elem] != ''
        filtered['transfertype'] = filters['transfertype'] != 'no selection'
        filtered['status'] = filters['status'] != 'no selection'
        conn = get_db_connection()
        cursor = conn.cursor()
        log_worked, errormessage, log = get_log(cursor,userID,filters,filtered)
        conn.close()
        filters['logtype'] = filters['logtype'] + "Log"
        if log_worked:
            if filtered['fromdate']:
                filters['fromdate'] = fixdate(filters['fromdate'])
                filters['todate'] = fixdate(filters['todate'])
            return render_template("logview.html", userID=userID,filters=filters,filtered=filtered, log=log)
        else:
            return render_template("logs.html", userID=userID,log_selection='',message=errormessage)
    else:
        userID = session['user_id']
        return render_template("logs.html", userID=userID,log_selection='',message='')

@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    if request.method == "POST":
        userID= session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor()
###
        #Amount to deposit
        amount = request.form.get('amount')
        amount = float(amount)
        #seeing whether they clicked default or other bank
        radio = request.form.get("bank")
        #Radio returns "otherbank" if user has no bank linked
        #Radio returns "defaultbank" if user has bank linked and checks default bank
        #Radio returns "otherbank" if user has bank linked and checks other bank
        newbank_hasnobank = request.form.get("newbank_hasnobank")
        #If this is true then user has bank linked
        if newbank_hasnobank == '':
            hasbank = True
            if radio == "otherbank":
                #if clicked other bank, get the new bank ID
                bankID = request.form.get("newbank")
                makedefault = request.form.get("makedefault")
                makedefault = makedefault == "makedefault"
                if makedefault:
                    deposit_worked, message = linkbanknoprint(userID,bankID,cursor)
                    if not deposit_worked:
                        bankID = getbank(userID,cursor)
                        bankID = "*****" + bankID[5:]
                        return render_template("deposit.html",hasbank=True,bankID=bankID,deposit_worked=deposit_worked,message=message)
                    else:
                        bankID = "*****" + bankID[5:]
            else:
                #if clicked default, store the default bankID
                makedefault = False
                bankID = getbank(userID,cursor)
                bankID = "*****" + bankID[5:]
        #this is the case that the user has no bank but wants to deposit
        else:
            makedefault = request.form.get('makedefault_hasnobank')
            makedefault = makedefault == "makedefault_hasnobank"
            hasbank = makedefault
            bankID = request.form.get('newbank_hasnobank')
            if makedefault:
                deposit_worked, message = linkbanknoprint(userID,bankID,cursor)
                if not deposit_worked:
                    return render_template("deposit.html",hasbank=False,bankID=bankID,deposit_worked=deposit_worked,message=message)
                else:
                    bankID = "*****" + bankID[5:]
        deposit_worked,message = depositnoprint(userID,amount,cursor)
        conn.commit()
        conn.close()
        return render_template("deposit.html",hasbank=hasbank,bankID=bankID,deposit_worked=deposit_worked,message=message)
    else:
        userID= session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        bankID = getbank(userID,cursor)
        hasbank = bankID != '*'
        if hasbank:
            bankID = "*****" + bankID[5:]
        conn.close()
        return render_template("deposit.html",hasbank=hasbank,bankID=bankID,message='')