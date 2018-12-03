#!/usr/bin/python
# -*- coding: utf-8 -*-
# Project File: Python 2.x or 3.x

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
from hashlib import sha256

"""blockchain.py incorporates cryptography
   into python.

   Example:

   blockchain = Blockchain()
   block = Block("some data",1)
   blockchain.mine(block)
   print(blockchain.chain)

"""

#get the update hash of arguments
def updatehash(*args):
    hashing_text = ""; h = sha256()
    for arg in args:
        hashing_text += str(arg)

    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()


#block object definition
class Block():
    data = None
    hash = None; nonce = 0
    previous_hash = "0" * 64

    #specify data and block number on instance
    def __init__(self,data,number=0):
        self.data = data
        self.number = number

    #hash a block using updatehash
    def hash(self):
        return updatehash(
            self.previous_hash,
            self.number,
            self.data,
            self.nonce
        )

    #when printing a block
    def __str__(self):
        return str("Block#: %s\nHash: %s\nPrevious:" +
            " %s\nData: %s\nNonce: %s\n" %(
            self.number,
            self.hash(),
            self.previous_hash,
            self.data,
            self.nonce
            )
        )


#blockchain object definition
class Blockchain():
    difficulty = 4

    #specify previous blockchain on instance
    def __init__(self,chain=[]):
        self.chain = chain

    #add a block to the chain
    def add(self, block):
        self.chain.append({
            'hash': block.hash(),
            'previous': block.previous_hash,
            'number': block.number,
            'data': block.data,
            'nonce': block.nonce
        })

    #find the correct nonce to satisfy the difficulty
    def mine(self, block):
        try: block.previous_hash = self.chain[-1].get('hash')
        except IndexError: pass

        while True: #loop until correct nonce found
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block); break
            else:
                block.nonce += 1


#find if a list is the majority of other lists
def ismajority(item,p,lists):
    counter = 0
    for l in lists:
        if l[p] == item:
            counter +=1

    if counter > len(lists)/2:
        return True


#get a list of the valid blockchains
def getvalidblockchains(chains):
    invalid_chains = []; valid_chains = []

    for blockchain in chains:
        for i in range(len(blockchain)):
            if not ismajority(blockchain[i],i,chains):
                invalid_chains.append(blockchain); break

        if blockchain not in invalid_chains:
            valid_chains.append(blockchain)

    return valid_chains


#testing the blockchain
if __name__ == '__main__':
    test_1 = ["hello","bye","word"]
    test_2 = ["hello","bye","word"]
    test_3 = ["hello","no","word"]
    test_4 = ["wait","bye","hey"]

    lists = [test_1,test_2,test_3,test_4]
    print(getvalidblockchains(lists))

    blockchain = Blockchain()
    database = ["hello","bye","hey"]

    num = 0

    for data in database:
        num += 1
        blockchain.mine(Block(data, num))

    print(blockchain.chain)
