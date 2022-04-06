# Venmo.py
**By Ishan Balakrishnan & Sukhm Kang**

This project recreates several of the core commands present in the Venmo application (https://venmo.com/), while managing a central database of user information and recording transaction histories for users within the payment ecosystem. The purpose of this project was to explore the ways a company like Venmo manages a major database while retrieving information from its databases to perform a multitude of commands in a way that optimizes for efficient runtime and storage.

**Visit the fully functional website [here](https://venmoproject.pythonanywhere.com/)!**

<img src="https://github.com/SukhmKang/passion-projects/blob/main/Venmo.py%20Image.png" width="350">

## Built With

**Python** (https://www.python.org/) \
**Flask** (https://flask.palletsprojects.com/en/2.0.x/) \
**Bootstrap** (https://getbootstrap.com/) \
**Javascript** (https://www.javascript.com/) \
**SQLite** (https://www.sqlite.org/index.html)

## Commands

### Overview

Our project enables users to create and operate accounts within a payment environment similar to Venmo's. These commands will allow users to friend users, complete transactions (pay, request, deposit, transfer, etc.), configure settings, and view filterable logs of transactions within their Venmo ecosystem.

### Descriptions & Usage

**```Homepage```**\
Description: The homepage hosts a variety of core features for the user. The user can see their profile, including their balance and profile picture. On the homepage, the user also has access to previews of all 5 logs offered by the program. The user can navigate to the ```Deposit```, ```Pay or Request```, and ```Transfer``` pages directly from the profile card.

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
Description: On the settings page, the user can ```verify``` their account, ```link``` a bank, set a ```default privacy```, and change their ```password```.

<img src="https://github.com/SukhmKang/venmo-project/blob/main/Screenshots/Settings.png" width="500">

**```Verification```**\
Description: As mentioned before, users can ```verify``` their account from the ```Settings``` page. Verification is crucial to the payment ecosystem, as users who have not verified their account cannot make ```Transfers``` and are subject to stricter weekly payment limits than verified users.

<img src="https://github.com/SukhmKang/venmo-project/blob/main/Screenshots/Verification.png" width="500">

**```personalLog```**\
Description: The ```personalLog``` displays payments directly involving the user and bank transfers. For the ```personalLog``` as well as the rest of the logs, the user can apply a variety of filters so that the log only shows the payments that the user wants to see.

<img src="https://github.com/SukhmKang/venmo-project/blob/main/Screenshots/Filters.png" width="500">

**```friendLog```**\
Description: The ```friendLog``` displays payments directly involving the user as well as ```Friends Only``` payments involving at least one of the user's friends.

**```globalLog```**\
Description: The ```globalLog``` displays all of the payments in the ```personalLog``` and ```friendLog``` in addition to all ```Public``` payments on the platform.

**```requestLog```**\
Description: The ```requestLog``` displays all of the user's incoming and outgoing requests. The log shows whether a request is  ```pending```, ```accepted```, or ```denied```.

<img src="https://github.com/SukhmKang/venmo-project/blob/main/Screenshots/Request%20Log.png" width="500">

**```transferLog```**\
Description: The ```transferLog``` displays all of the user's bank transfers.

## Backend Features

### Database

The central database (venmo.db) contains a Users table and a paymentLog table.

**Users**

<img src="https://github.com/SukhmKang/venmo-project/blob/main/Screenshots/users.png" width="500">

**paymentLog**

<img src="https://github.com/SukhmKang/venmo-project/blob/main/Screenshots/paymentLog.png" width="500">

### Payment Limits

The Venmo app has several payment limits depending on the account type and verification status of the account. Many of the payment limits are spending/receiving limits on a per-week basis. Every time a user attempts to makes a payment on our app, the application automatically checks if they or the recipient have exceeded any payment limits before permitting the transaction.

<img src="https://github.com/SukhmKang/venmo-project/blob/main/Screenshots/Payment%20Limits.png" width="500">

### Filtering
All log commands, ```friendLog```, ```personalLog```, ```requestLog```, ```transferLog```, and ```globalLog```, allow users to input optional filters for the data presented in the log. Users have the option to apply (and stack) any of the following filters with ease: 

**```above```** filters payments keeping only the transactions that are above a certain payment amount \
**```below```** filters payments keeping only the transactions that are above a certain payment amount \
**```range```** filters payments keeping only the transactions with an amount  within a certain interval \
**```days```** filters payments keeping only the transactions that are within the last n number of days \
**```daterange```** filters payments within a date range \
**```tags```** filters payments keeping only the transactions that are "tagged" with a specific tag \
**```sender```** filters payments keeping only the transactions that are from a specific sender \
**```recipient```** filters payments keeping only the transactions that are to a specific recipient \
**```message```** filters payments keeping only the transactions that have a specific payment message \
**```messagecontaints```** filters payments keeping only the transactions that have a payment message which includes a certain string

Certain filters only apply to specific logs; for example, transfers do not have messages and thus cannot be filtered by ```message``` or ```messagecontains```. Furthermore, requests in the ```requestLog``` can be filtered by whether they were ```accepted```, ```denied```, or ```pending```.

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
