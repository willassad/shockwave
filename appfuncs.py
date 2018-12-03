#!/usr/bin/python
# -*- coding: utf-8 -*-
# Project File: Python 2.x or 3.x

# DESCRIPTION
"""appfuncs.py is the access to
   databases and the blockchain.
"""

__author__ = "Will Assad"
__copyright__ = "Copyright 2018, Shockwave"
__credits__ = ["Will Assad"]
__developers__ = ["willassad"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Will Assad"
__email__ = "willassadcode@gmail.com"
__status__ = "Production"

#IMPORTS
try: from app import mysql, session
except ImportError as e: print(e)

from blockchain import Block, Blockchain, updatehash

try:
    import httplib
except Exception:
    import http.client as httplib


#check if the user is connected to the internet
def internet_connected():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/"); conn.close()
        return True
    except Exception:
        conn.close()
        return False

#create ab object of a mysql table for easy access
class Table():
    #specify table name on instance
    def __init__(self,table_name):
        self.table = table_name

    #returns a dictionary of all data in the table
    def getall(self):
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s" %self.table)
        data = cur.fetchall(); return data

    #gets a value from the table
    def getone(self,search,value):
        data = {}; cur = mysql.connection.cursor()
        result = cur.execute(
            "SELECT * FROM %s WHERE %s = \"%s\"" %(self.table,search,value)
        )

        if result > 0: data = cur.fetchone()
        cur.close(); return data

    #deletes a value from the table
    def deleteone(self,search,value):
        cur = mysql.connection.cursor()
        cur.execute("DELETE from %s where %s = \"%s\"" %(self.table,search,value))
        mysql.connection.commit(); cur.close()

    #deletes the table from the database
    def drop(self):
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE %s" %self.table)
        cur.close()

#simplify execution of sql code
def sql_raw(execution):
    cur = mysql.connection.cursor()
    cur.execute(execution)
    mysql.connection.commit()
    cur.close()

#check if a table is new to the database
def isnewtable(tableName):
    cur = mysql.connection.cursor()

    try:
        result = cur.execute("SELECT * FROM %s" %tableName)
        cur.close()
    except:
        return True
    else:
        return False

#get the last copy of the blockchain
def getLastBlockchain():
    blockchain = Table("blockchain")
    unsorted = list(blockchain.getall())
    sorted = []
    for block in unsorted:
        if block.get('number') is not None:
            sorted.insert(int(block.get('number'))-1,block)

    return sorted

#add a transaction to the blockchain
def addTransaction(sender,receiver,amount,bought=False):
    last_blockchain = getLastBlockchain()
    blockchain = Blockchain(last_blockchain)
    num = len(last_blockchain) + 1

    if bought: data = "%s OBTAINED %s" %(receiver,amount)
    else: data = "%s --> %s (%s)" %(sender,receiver,amount)
    blockchain.mine(Block(data, num))
    last = blockchain.chain[-1]

    sql_raw(
    "INSERT INTO blockchain(number,hash,previous,data,nonce)" +
    "VALUES(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" %(
        last.get('number'),
        last.get('hash'),
        last.get('previous'),
        last.get('data'),
        last.get('nonce')
        )
    )

#verify if the blockchain is not corrupt
def verifyBlockchain():
    blockchain = getLastBlockchain()#; print(blockchain)

    for n in range(len(blockchain)):
        block_hash = updatehash(
            blockchain[n].get('previous'),
            blockchain[n].get('number'),
            blockchain[n].get('data'),
            blockchain[n].get('nonce')
        )

        if block_hash != blockchain[n].get('hash'):
            return False
        elif block_hash[:4] != "0000":
            return False

        if n < len(blockchain)-1:
            if block_hash != blockchain[n+1].get('previous'):
                return False

    return True


#check if username is not taken upon registration
def isnewuser(username):
    users = Table("users")
    data = users.getall()
    usernames = [user.get('username') for user in data]

    return False if username in usernames else True

#send money to a user
def send_money(username,amount,bought=False):
    balances = getbalances()

    if bought:
        if amount == 0: session['balance'] = amount
        else: session['balance'] += amount
    else:
        session['balance'] -= amount
        receiver_balance = balances.get(username) + amount

    if bought: addTransaction("ADMIN",username,amount,bought)
    else: addTransaction(session.get('username'),username,amount,bought)


#get a dicitionary of balances of each user
def getbalances():
    blockchain = Table("blockchain")
    blockchain = blockchain.getall()
    transactions = [block.get('data') for block in blockchain]

    balances = {}

    for transaction in transactions:
        if "OBTAINED" in transaction:
            username, amount = transaction.split(" OBTAINED ")
            if balances.get(username) is None:
                balances[username] = int(amount)
            else:
                balances[username] += int(amount)

        elif "-->" in transaction:
            sender,receiver_data = transaction.split(" --> ")
            receiver,amount = receiver_data.split(" (")
            amount = int(amount.replace(")",""))
            balances[sender] -= int(amount)

            if balances.get(receiver) is None:
                balances[receiver] = int(amount)
            else:
                balances[receiver] += int(amount)

    return balances
