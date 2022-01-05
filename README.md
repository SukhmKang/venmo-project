# Venmo Python Project

This project attempts to mimic several of the core commands present in the Venmo application (https://venmo.com/), while managing a central database of user information ([users.db](#user-database-usersdb)) and recording transaction histories ([paymentLog.db](#transactions-database-paymentlogdb)) for users within the payment ecosystem. The purpose of this project was to explore the ways a company like Venmo manages a major database while retrieving information from its databases to perform a multitude of commands in a fast and space-efficient way.

<img src="https://github.com/SukhmKang/passion-projects/blob/main/Venmo.py%20Image.png" width="350">

## Built With

**Python** (https://www.python.org/) \
**SQLite** (https://www.sqlite.org/index.html)

## Commands

### Overview

Our project enables users to create and operate accounts within an environment similar to Venmo's. These commands will allow users to friend users, complete transactions (pay, request, deposit, transfer, etc.), configure settings, and view logs of transactions within their Venmo ecosystem.

Users have access to several commands including:
```
cmds = ["pay","linkbank","override","request","transfer","deposit","acceptrequest","unrequest","denyrequest",
"friend","balance","adduser","verify","unfriend","setprivacy","updateprivacy","transactionprivacy","globallog",
"friendlog","personallog","requestlog","viewprofile"]
```
### Descriptions & Usage

Note: several of the commands below can take optional arguments; optional parameters will be indicated using the following format: \
```cmd arg1 arg2 [-optionalParamName optionalParamValue]```

Commands:


**```venmo.py pay senderID recipientID amount message [-tag tag -privacy privacy]```**\
Description: The pay command allows a user to send a payment to another user in the payment ecosystem. Every payment includes an amount and payment message (taken as input from the sender), and a date and unique paymentID (calculated by our program). Senders have the option to specify a ```-privacy``` for the payment or utilize their default privacy settings. Senders also have the option to ```-tag``` payments to one of the following categories:

```tags = ["food", "groceries", "rent", "utilities", "sports", "fun", "transportation", "drinks", "business", "tickets", "gift", "gas"]```

**```venmo.py linkbank userID bankID```**\
Description: The linkbank command allows a new user to link a bank to their Venmo account using their bankID (a 9-digit routing number). A user must link their bank as a precursor to using other commands such as ```deposit```.

**```venmo.py override userID password bankID```**\
Description: The override command allows a user to change their bank settings and switch to a new bankID. Unlike the linkbank command (which is meant for first-time use when a user needs to initially setup their bank), ```override``` is password-protected. In order for the user's bankID changes to be saved, the password must be entered correctly. 

**```venmo.py request userID friendID amount message [-tag tag]```**\
Description: The request command allows a user to request a payment from another user in the payment ecosystem. Every request includes an amount and request message (taken as input from the requester), and a date and requestID (calculated by our program). Senders have the option to specify a ```-tag``` for the request. Once the request is sent, the requested user will be able to ```acceptrequest``` or ```denyrequest```, and the requester will always have the option to ```unrequest```.

**```venmo.py transfer userID amount [-type instant or -type "no fee"]```**\
Description:

**```venmo.py deposit userID amount```**\
Description:

**```venmo.py acceptrequest senderID paymentID [-privacy privacy]```**\
Description:

**```venmo.py unrequest userID paymentID```**\
Description:

**```venmo.py denyrequest senderID paymentID```**\
Description:

**```venmo.py friend userID friendID'```**\
Description:

**```venmo.py balance userID password```**\
Description:

**```venmo.py adduser userID password accounttype```**\
Description:

**```venmo.py verify userID password SSN```**\
Description:

**```venmo.py unfriend userID friendID```**\
Description:

**```venmo.py setprivacy userID privacy```**\
Description:

**```venmo.py updateprivacy userID password privacy```**\
Description:

**```venmo.py transactionprivacy userID paymentID privacy```**\
Description:

**```venmo.py globallog userID [filters]```**\
Description:

**```venmo.py friendlog userID friendID [filters]```**\
Description:

**```venmo.py personallog userID [filters]```**\
Description:

**```venmo.py requestlog userID [-type outgoing or -type incoming]```**\
Description:

**```venmo.py viewprofile userID```**\
Description: The viewprofile command allows a user to see their account profile which includes their userID, balance, verification status, number of friends, date of account creation, and aggregate fees. See examples of [user profiles](#user-profiles) below.

## Example Database

### User Database: users.db

Here is an example of users.db:

![](https://github.com/SukhmKang/passion-projects/blob/main/Venmo%20Users.db.png)

### Transactions Database: paymentLog.db

Here is an example of paymentLog.db:

![](https://github.com/SukhmKang/passion-projects/blob/main/Venmo%20paymentLog.db.png)

## Example Output

### Transaction Logs

Here is an example of the output printed by specific commands in our program once the payment system is loaded using Commands.txt (a starter script which generates users and performs several transactions).

COMMAND:

```
python3 venmo.py globallog ishan
```
This command will print the ```globallog``` viewable for a given userID. In other words, all payments that are set to ```"Public"``` or are ```"Friends Only"``` and include one of userID's friends or are ```"Private"``` but involve the userID as a sender or recipient, will be logged. 

OUTPUT:
```
======
SUKHM paid ISHAN $100.00
Date: 2022-01-04 16:03:12
Message: hi
ID: 8402874417959245168
Privacy: Private
======

======
SUKHM paid ISHAN $4.00
Date: 2022-01-04 16:03:12
Message: hi
ID: -4307748576687562439
Privacy: Private
======

======
BOB paid ROB $0.01
Date: 2022-01-04 16:03:12
Message: haha
ID: -4058719667198402045
Privacy: Public
======

======
ROB paid BOB $1.00
Date: 2022-01-04 16:03:12
Message: hi
ID: 3306642345074302835
Privacy: Public
======

======
ROB paid WILL $11.00
Date: 2022-01-04 16:03:12
Message: hi
ID: 74808842343309024
Privacy: Public
======
```
### Filtering
Like all other log commands (```friendLog```, ```personalLog```, ```requestLog```), the ```globalLog``` also allows users to input optional input to filter the data presented in the log. Users have the option to apply (and even stack) any of the following filters: 

```filters = ["-above","-below","-range","-days","-tags","-sender","-recipient","-message","-messagecontains"]```

**```-above```** filters payments keeping only the transactions that are above a certain payment amount \
**```-below```** filters payments keeping only the transactions that are above a certain payment amount \
**```-range```** filters payments keeping only the transactions with an amount  within a certain interval \
**```-days```** filters payments keeping only the transactions that are within the last n number of days \
**```-tags```** filters payments keeping only the transactions that are "tagged" with a specific tag \
**```-sender```** filters payments keeping only the transactions that are from a specific sender \
**```-recipient```** filters payments keeping only the transactions that are to a specific recipient \
**```-message```** filters payments keeping only the transactions that have a specific payment message \
**```-messagecontaints```** filters payments keeping only the transactions that have a payment message which includes a certain string


Let's say a user may want to use the -range and -sender filters to specify a payment with an amount between $5 and $15 sent by Rob. 

To do this, the user would input the following command:

COMMAND:

```
python3 venmo.py globallog ishan -sender rob -range 5-15
```
This command will print the new ```globallog``` after applying the specific filters. After the filtering, only one payment remains in the log.

OUTPUT:
```
======
ROB paid WILL $11.00
Date: 2022-01-04 16:03:12
Message: hi
ID: 74808842343309024
Privacy: Public
======
```

### User Profiles
User profiles showcase several important attributes of a Venmo user, as saved in the ([users.db](#user-database-usersdb)) or calculated from the ([paymentLog.db](#transactions-database-paymentlogdb)). This includes the user's userID, balance, verification status, number of friends, date of account creation, and total fees paid.

COMMAND:

```
python3 venmo.py userprofile ariana
```

OUTPUT:
```
==================
VENMO User Profile
==================
@ARIANA - √erified
$700.00
1 friend
joined 2022-01-04
==================
```

COMMAND:

```
python3 venmo.py userprofile john
```

OUTPUT:
```
==================
VENMO User Profile
==================
@JOHN - unverified
$0.00
11 friends
joined 2022-01-04
==================
```

COMMAND:

```
python3 venmo.py userprofile bob
```

OUTPUT:
```
==================
VENMO User Profile
==================
@BOB - √erified
$2506.93
No friends yet!
ƒees: $15.00
joined 2022-01-04
==================
```


## Authors & Contact Information

This project was authored by **Sukhm Kang** and **Ishan Balakrishnan**.

**Sukhm Kang**\
Mathematics @ The University of Chicago\
https://www.linkedin.com/in/sukhm-kang


**Ishan Balakrishnan**\
Computer Science & Business @ University of California, Berkeley\
https://www.linkedin.com/in/ishanbalakrishnan

Feel free to reach out to either one of us by email @ ishan.balakrishnan(at)berkeley.edu or sukhm.kang(at)uchicago.edu! 

## Acknowledgments

The inspiration behind several of the commands and text (fee rates, spending limits) present in this project comes directly from Venmo (https://venmo.com/).
