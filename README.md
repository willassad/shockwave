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
$ python app.py
```
Shockwave cryptocurrency is now up and running!

## Prerequisites
Make sure you have Python 3 installed. Install the following dependencies.
```
$ pip install Flask
$ pip install simple-crypt
$ pip install passlib
$ pip install flask_mysqldb
$ pip install functools
$ pip install wtforms
```
Make sure you have mysql (if you don't click here: https://www.youtube.com/watch?v=UcpHkYfWarM). 

Create a database 'shockwave' in mysql.
```
mysql> CREATE DATABASE shockwave;
mysql> use shockwave;
mysql> CREATE TABLE users(name varchar(30), email varchar(30), username varchar(20), password varchar(50));
mysql> CREATE TABLE blockchain(number varchar(30), hash varchar(68), previous varchar(68), data varchar(100), nonce varchar(30));
```

## Built With
HTML - Front end web framework

CSS - Front end styling

JS - Backend framework

Python - Backend application


## Authors
Will Assad - Entire Project

## License
This project is licensed under the MIT License - see the LICENSE file for details
