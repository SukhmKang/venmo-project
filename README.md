# Venmo Python Project

This project attempts to mimic several of the core commands present in the Venmo application (https://venmo.com/), while managing a central database of user information ([users.db](#user-database-usersdb)) and recording transaction histories ([paymentLog.db](#transactions-database-paymentlogdb))of the users within the ecosystem. The purpose of this project was to explore the ways a company like Venmo manages a major database while retrieving information from it to perform several commands in a faste and space-efficient way.


## Built With

**Python** (https://www.python.org/) \
**SQLite** (https://www.sqlite.org/index.html)

## Commands

**Overview**

Our project enables users to create and operate accounts within an environment similar to Venmo's. These commands will allow users to friend users, complete transactions (pay, request, deposit, transfer, etc.), configure settings, and view logs of transactions within their Venmo ecosystem.

Users have access to several commands including:
```
cmds = ["pay","linkbank","override","request","transfer","deposit","acceptrequest","unrequest","denyrequest",
"friend","balance","adduser","verify","unfriend","setprivacy","updateprivacy","transactionprivacy","globallog",
"friendlog","personallog","transactionlog","requestlog","viewprofile"]
```
**Descriptions & Usage**

## Example Database

### User Database: users.db

Here is an example of users.db:

### Transactions Database: paymentLog.db

Here is an example of paymentLog.db:

## Example Output

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

## Authors & Contact Information

This project was authored by **Sukhm Kang** and **Ishan Balakrishnan**.

**Sukhm Kang**\
Mathematics @ The University of Chicago\
https://www.linkedin.com/in/sukhm-kang


**Ishan Balakrishnan**\
Computer Science & Business @ University of California, Berkeley\
https://www.linkedin.com/in/ishanbalakrishnan

Feel free to reach out to either one of us ishan.balakrishnan(at)berkeley.edu or sukhm.kang(at)uchicago.edu! 

## Acknowledgments

The inspiration behind several of the commands and text (fee rates, spending limits 


) present in this project comes directly from Venmo (https://venmo.com/).
