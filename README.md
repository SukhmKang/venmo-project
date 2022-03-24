# Venmo.py
**By Ishan Balakrishnan & Sukhm Kang**

This project recreates several of the core commands present in the Venmo application (https://venmo.com/), while managing a central database of user information and recording transaction histories for users within the payment ecosystem. The purpose of this project was to explore the ways a company like Venmo manages a major database while retrieving information from its databases to perform a multitude of commands in a way that optimizes for efficient runtime and storage.

Visit the fully functional website [here](https://venmoproject.pythonanywhere.com/)!

<img src="https://github.com/SukhmKang/passion-projects/blob/main/Venmo.py%20Image.png" width="350">

## Built With

**Python** (https://www.python.org/) \
**Flask** (https://flask.palletsprojects.com/en/2.0.x/) \
**Bootstrap** (https://getbootstrap.com/) \
**SQLite** (https://www.sqlite.org/index.html)

## Commands

### Overview

Our project enables users to create and operate accounts within a payment environment similar to Venmo's. These commands will allow users to friend users, complete transactions (pay, request, deposit, transfer, etc.), configure settings, and view filterable logs of transactions within their Venmo ecosystem.

### Descriptions & Usage

Features:

**```Homepage```**\
Description: The homepage hosts a variety of core features for the user. The user can see their profile, including their balance and profile picture. On the homepage, the user also has access to previews of all 5 logs offered by the program.

<img src="https://github.com/SukhmKang/venmo-project/blob/main/Screenshots/Homepage.png" width="500">

**```Payment```**\
Description: The pay command allows a user to send a payment to another user in the payment ecosystem. Every payment includes an amount and payment message (taken as input from the sender), a date, and a unique paymentID (calculated by our program). Senders have the option to specify a ```privacy``` for the payment or utilize their default privacy settings. Senders also have the option to ```tag``` payments to one of the following categories:

```tags = ["food", "groceries", "rent", "utilities", "sports", "fun", "transportation", "drinks", "business", "tickets", "gift", "gas"]```

**```Linking a Bank```**\
Description: Users can link a bank to their Venmo account using their bankID (a 9-digit routing number). A user must link their bank as a precursor to using other features such as ```deposit``` and ```transfer```. Users can link a bank from multiple parts of the site, including the ```settings```, ```deposit```, and ```transfer``` pages.

**```Requests```**\
Description: Users can request a payment from another user in the payment ecosystem. Every request includes an amount and request message (taken as input from the requester), and a date and requestID (calculated by our program). Senders have the option to specify a ```tag``` for the request. Once the request is sent, the requested user will be able to ```accept request``` or ```deny request```.

**```Friends```**\
Description: Users can send friend requests to other users in the ecosystem. Once a friend request is accepted, both users can pay and request each other and can also see Friends Only transactions from each other in their ```friendLog``` and ```globalLog```. Friends can be selected from the ```social``` page, which auto-populates the ```pay/request``` form with the friend's name.

**```Accepting and Rejecting Requests```**\
Description: On the requests page (accessible by clicking the notification bell on the ```home``` page), users can accept incoming payment requests and friend requests.

<img src="https://github.com/SukhmKang/venmo-project/blob/main/Screenshots/Accept:Deny%20Requests.png" width="500">

**```Bank Transfers```**\
Description: Transfers allows a user to transfer money out of their Venmo balance and into their bank account. Just like in Venmo, users have two options when initiating a transfer: "instant" and "no fee." Transfers are viewable in a user's ```personalLog``` and ```transferLog``` and fees paid are tracked on a user's profile (accessible on the ```home``` page).

**```Deposit```**\
Description: Deposit allows users to deposit money into their Venmo balance. To deposit money into their Venmo account, a user must first link a bank and verify their account. If users do not have a bank linked, the deposit page give them option to input a bank temporarily, with the option of making it a default bank. 

<img src="https://github.com/SukhmKang/venmo-project/blob/main/Screenshots/Make%20Default.gif" width="500">

**```Settings```**\
Description: On the settings page, the user can 

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

### User Database: Users

Here is an example of our users table:

![](https://github.com/SukhmKang/passion-projects/blob/main/Venmo%20Users.db.png)

### Transactions Database: paymentLog

Here is an example of our paymentLog table:

![](https://github.com/SukhmKang/passion-projects/blob/main/Venmo%20paymentLog.db.png)

## Example Output

### Transaction Logs

Here is an example of the output printed by specific commands in our program once the payment system is loaded using Commands.txt (a starter script which generates users and performs several transactions).

**COMMAND:**

```
python3 venmo.py globallog Lukas
```
This command will print the ```globallog``` viewable for a given userID. In other words, all payments that are set to ```"Public"``` or are ```"Friends Only"``` and include one of userID's friends or are ```"Private"``` but involve the userID as a sender or recipient, will be logged. 

**OUTPUT:**
```
======
CADENCE paid LEIGHTON $39.00
Date: 2022-01-05 19:24:25
Message: neighbor
ID: 4912021424446041479
Privacy: Public
Tag: gas
======

======
NATHALIA paid RAYMOND $32.00
Date: 2022-01-05 19:24:25
Message: wrote near arrange gray
ID: -5995160770132735197
Privacy: Public
======

======
ELISHA paid LEIGHTON $17.00
Date: 2022-01-05 19:24:25
Message: seeing image include friendly face
ID: 8785650049271825540
Privacy: Public
======

======
RAYMOND paid JAYCE $2.00
Date: 2022-01-05 19:24:25
Message: already brief reach
ID: -150183031060747061
Privacy: Friends Only
Tag: sports
======

======
LUPITA paid RAYMOND $33.00
Date: 2022-01-05 19:24:25
Message: related him mouth carried badly
ID: 4281393501062655380
Privacy: Friends Only
Tag: drinks
======

======
LUPITA paid ESTEFANIA $40.00
Date: 2022-01-05 19:24:25
Message: quick wing repeat minute matter
ID: 235882096320024938
Privacy: Friends Only
Tag: fun
======

======
CHARLEY paid LUKAS $4.00
Date: 2022-01-05 19:24:25
Message: tune
ID: 7830547338156538219
Privacy: Private
Tag: drinks
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


Let's say a user may want to use the -above and -sender filters to specify a payment with an amount above $35 sent by Lupita. 

To do this, the user would input the following command:

**COMMAND:**

```
python3 venmo.py globallog Lukas -sender Lupita -above 35
```
This command will print the new ```globallog``` after applying the specific filters. After the filtering, only one payment remains in the log.

**OUTPUT:**
```
======
LUPITA paid ESTEFANIA $40.00
Date: 2022-01-05 19:24:25
Message: quick wing repeat minute matter
ID: 235882096320024938
Privacy: Friends Only
Tag: fun
======
```

Users can also use the **```requestlog```** to view incoming and outgoing requests, including their respective request status (ccepted, denied, pending, or cancelled).

**COMMAND:**

```
python3 venmo.py requestlog ashley -range 20-50
```

**OUTPUT:**
```
===============
PENDING REQUEST
KYRA requested $49.00 from ASHLEY
Date: 2022-01-05 14:47:07
Message: present forgot choice
ID: -8828219609105870469
Tag: food
===============

===============
ACCEPTED REQUEST
MIRANDA accepted ASHLEY's request for $28.00
Date: 2022-01-05 14:47:07
Message: visitor ring fed contrast
ID: -4572332181465126335
===============

===============
CANCELLED REQUEST
ASHLEY cancelled their request for $34.00 from COEN
Date: 2022-01-05 14:47:07
Message: smaller
ID: -6263499498269279458
Tag: groceries
===============
```

Users can also use the **```friendlog```** to see specific transactions involving one of their friends (similar to the transaction history that a user sees on Venmo after clicking on a friend's profile:

**COMMAND:**

```
python3 venmo.py friendlog eliza -below 40
```

**OUTPUT:**
```
=======
ELIZA paid MARCELLO $10.00
Date: 2022-01-05 19:32:37
Message: expect thick hand tropical
ID: 646440887148715387
Privacy: Public
Tag: food
=======

=======
ELIZA paid ALEXA $22.00
Date: 2022-01-05 19:32:37
Message: using
ID: -3226112198171525621
Privacy: Friends Only
Tag: sports
=======

=======
KAYSEN paid ELIZA $16.00
Date: 2022-01-05 19:32:37
Message: already greatest clock character
ID: 7255611750700585485
Privacy: Public
Tag: rent
=======

=======
JOVIE paid ELIZA $36.00
Date: 2022-01-05 19:32:37
Message: sweet our taken deep base
ID: -6666593477264811232
Privacy: Public
Tag: business
=======

=======
FOSTER paid ELIZA $3.00
Date: 2022-01-05 19:32:37
Message: shinning court volume
ID: 8977508245405188969
Privacy: Public
Tag: food
=======

=======
ELIZA paid LUKAS $3.00
Date: 2022-01-05 19:32:37
Message: stepped bridge all boy idea
ID: 1399052944502408428
Privacy: Public
=======
```

The last log users can access is the **```personallog```** which tracks all of a user's own transactions, including their bank transfers. 

**COMMAND:**

```
python3 venmo.py personallog lukas
```

**OUTPUT:**
```
=======
LUKAS paid RAYMOND $4.00
Date: 2022-01-05 19:39:20
Message: mine party running rabbit
ID: 1876582270564654817
Privacy: Public
Tag: tickets
=======

=======
FLORA paid LUKAS $40.00
Date: 2022-01-05 19:39:20
Message: buried
ID: 8027349983504459532
Privacy: Friends Only
Tag: fun
=======

=======
LUKAS transferred $888.00 to bank 867410893
No Fee Transfer
Date: 2022-01-05 19:38:15
ID: 1468992921269261560
=======

=======
LUKAS paid FOSTER $44.00
Date: 2022-01-05 19:39:21
Message: operation
ID: 2006268989207569363
Privacy: Public
Tag: sports
=======

=======
LUPITA paid LUKAS $34.00
Date: 2022-01-05 19:39:21
Message: broad frequently frozen leg three
ID: 8873442707971198000
Privacy: Friends Only
Tag: drinks
=======

=======
LUKAS transferred $798.00 to bank 867410893
Instant Transfer
Date: 2022-01-05 19:38:50
ID: -8942518831985827823
=======

=======
CHARLEY paid LUKAS $4.00
Date: 2022-01-05 19:39:21
Message: tune
ID: 5617351941942471040
Privacy: Private
Tag: drinks
=======
```

If Lukas  wanted to see just the balance transfers made to their bank, they could apply the ```-type``` filter and select to show only transfers. This would log just the two transfers Lukas made.

**COMMAND:**

```
python3 venmo.py personallog lukas -type transfers
```

**OUTPUT:**
```
=======
LUKAS transferred $888.00 to bank 867410893
No Fee Transfer
Date: 2022-01-05 19:38:15
ID: 1468992921269261560
=======

=======
LUKAS transferred $798.00 to bank 867410893
Instant Transfer
Date: 2022-01-05 19:38:50
ID: -8942518831985827823
=======

```

### User Profiles
User profiles showcase several important attributes of a Venmo user, as saved in the ([users.db](#user-database-usersdb)) or calculated from the ([paymentLog.db](#transactions-database-paymentlogdb)). This includes the user's userID, balance, verification status, number of friends, date of account creation, and total fees paid.

**COMMAND:**

```
python3 venmo.py userprofile ariana
```

**OUTPUT:**
```
==================
VENMO User Profile
==================
@ARIANA - √erified
$740.90
67 friends
joined 2022-01-04
==================
```

**COMMAND:**

```
python3 venmo.py userprofile john
```

**OUTPUT:**
```
==================
VENMO User Profile
==================
@JOHN - unverified
$2.31
41 friends
joined 2022-01-04
==================
```

**COMMAND:**

```
python3 venmo.py userprofile bob
```

**OUTPUT:**
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

Feel free to reach out to either one of us by email @ ishan.balakrishnan(at)berkeley.edu or sukhmkang(at)uchicago.edu! 

## Acknowledgments

The inspiration behind several of the commands and text (fee rates, spending limits) present in this project comes directly from Venmo (https://venmo.com/).
