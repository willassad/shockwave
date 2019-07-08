# Shockwave
Shockwave is a cryptocurrency made in python. It also contains a user interface where one can send money, deposit money, and view their current balance. Shockwave uses crytography (see blockchain.py) to send and verify transactions. Sending money will update the blockchain and each user's balances.

## Getting Started
To get started simply download this repository.

From the command line:

```
$ git clone https://github.com/willassad/shockwave
```

Once downloaded, switch into the source folder and run app.py
```
$ cd shockwave # This may be different for you
$ python app.py
```
Shockwave cryptocurrency is now up and running!

## Prerequisites

### Install mySQL
Note: You may skip this if you already have mySQL installed
```
$ brew install mysql 
$ brew tap homebrew/services
$ brew services start mysql
$ mysqladmin -u root password 'yourpassword' 
```

### Configure mySQL 
Start mySql session in terminal
```$ mysql -u root -p```

#### Create database and tables
``` 
mysql> 
       CREATE DATABASE shockwave;
       use shockwave;
       CREATE TABLE users(name varchar(30), email varchar(30), username varchar(20), password varchar(50));
       CREATE TABLE blockchain(number varchar(30), hash varchar(68), previous varchar(68), data varchar(100), nonce varchar(30));
```

#### Configure Database Config File
Update Line 41 in ```app.py``` with the password saved above

If you are having troubles install mySql, you may use the link below. 
https://www.youtube.com/watch?v=UcpHkYfWarM 

### Dependencies
Make sure you have Python 3 installed. Install the following dependencies.
``` 
pip3 install -r requirements.txt 
```

```  
# You can also install them manually

$ pip install Flask
  pip install simple-crypt
  pip install passlib
  pip install flask_mysqldb #mySql must be installed, see below
  pip install functools
  pip install wtforms
```

## Built With
HTML - Front end web framework

CSS - Front end styling

JS - Backend framework

Python - Backend application


## Authors
Will Assad - Entire Project

Devansh Kaloti - Installation Process


## License
This project is licensed under the MIT License - see the LICENSE file for details
