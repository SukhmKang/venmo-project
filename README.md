# Venmo Python Project

This project attempts to mimic several of the core commands present in the Venmo application (https://venmo.com/), while managing a central database of user information ([users.db](#user-database-usersdb)) and recording transaction histories ([paymentLog.db](#transactions-database-paymentlogdb)) for users within the payment ecosystem. The purpose of this project was to explore the ways a company like Venmo manages a major database while retrieving information from its databases to perform a multitude of commands in a fast and space-efficient way.


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

Note: several of the commands below can take optional arguments; optional parameters will be designated as follows: \
```cmd arg1 arg2 [-optionalParamName optionalParamValue]```

Commands:


**```venmo.py pay senderID recipientID amount message [-tag tag -privacy privacy]```**\
Description:

**```venmo.py linkbank userID bankID```**\
Description:

**```venmo.py override userID password bankID```**\
Description:

**```venmo.py request userID friendID amount message [-tag tag]```**\
Description:

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

**```venmo.py requestlog userID [outgoing or incoming]```**\
Description:

**```venmo.py viewprofile userID```**\
Description:

## Example Database

### User Database: users.db

Here is an example of users.db:

### Transactions Database: paymentLog.db

Here is an example of paymentLog.db:

## Example Output

### Transaction Logs

Here is an example of the output printed by specific commands in our program once the payment system is loaded using Commands.txt (a starter script which generates users and performs several transactions).

COMMAND:

```
python3 venmo.py globallog ishan
```
This command will print the ```globallog``` viewable for a given userID. In other words, all payments that are set to ```"Public"``` or are ```Friends Only``` and include one of userID's friends or are ```Private``` but involve the userID as a sender or recipient, will be logged. 

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

Like all other log commands (```friendLog```, ```personalLog```, ```requestLog```), the ```globalLog``` also allows users to input optional input to filter the data presented in the log. Users have the option to apply any of the following filters: 

Let's say a user may want to use the -range and -sender filters to specify a payment with an amount between $5 and $15 sent by ROB. 

To do this, the user could input the following command:

COMMAND:

```
python3 venmo.py globallog ishan -sender rob -range 5-15
```
This command will print the new ```globallog``` after applying the filters. We can now see just one payment in the log.

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
