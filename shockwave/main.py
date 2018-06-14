import hashlib
import datetime
from time import sleep
import getpass
import os

#BLOCKCHAIN

def checkBalance(currentAddress):
    whichUser = currentAddress
    fileName = whichUser+".txt"

    try:
        file = open(fileName, "r")
        for enteredValue in file:
            enteredValue = enteredValue.strip()
            enteredValue = enteredValue.strip("\n")
            enteredValue = enteredValue.strip("'")

        tempList = list(enteredValue)
        gap_pos = enteredValue.find(" ")

        for x in range(0,(gap_pos+1)):
            del tempList[0]

        print "\nYour current balance is %s SHK" %(int("".join(tempList)))
    except IOError:
        print "No current balance. Buy SHK on coinbase: "
        os._exit(1)


def transaction(currentAddress):
    fromAddress = currentAddress

    ask=raw_input("\n1. Send Money \n2. View Balance \n3. Quit \n")
    if ask=="1":
        toAddress = raw_input("\nSend to: ")
        if fromAddress==toAddress:
            sleep(3)
            print("Transaction cannot be completed: ")
            os._exit(1)
        amount = input("Amount: ")
        if amount<=0:
            sleep(2)
            print("Transaction cannot be completed: ")
            os._exit(1)

        #LEDGER
        fileName = "transactionhistory.txt"
        file = open(fileName, 'a')
        text= str(fromAddress)+str(toAddress)+str(amount)
        file.write("%s\n" %text)
        file.close()


        #WRITING BALANCE OF SENDER
        fileName = fromAddress+".txt"
        try:
            file = open(fileName, 'r')
            for enteredValue in file:
                enteredValue = enteredValue.strip()
                enteredValue = enteredValue.strip("\n")
                enteredValue = enteredValue.strip("'")

            tempList = list(enteredValue)
            gap_pos = enteredValue.find(" ")

            for x in range(0,(gap_pos+1)):
                del tempList[0]

            oldBalance = int("".join(tempList))

            if int(amount)>oldBalance:
                print "Insufficient funds: "
                os._exit(1)

            newBalance = oldBalance - int(amount)
            file.close()

            file = open(fileName, "w")
            text= fromAddress+" "+str(newBalance)
            file.write("%s\n" %text)
            file.close()

            transact = str(fromAddress)+str(toAddress)+str(amount)

        except IOError:
            print "Insufficient funds: "
            os._exit(1)

        #WRITING BALANCE OF RECEIVER

        fileName = toAddress+".txt"

        try:
            file = open(fileName, 'r')
            for enteredValue in file:
                enteredValue = enteredValue.strip()
                enteredValue = enteredValue.strip("\n")
                enteredValue = enteredValue.strip("'")

            tempList = list(enteredValue)
            gap_pos = enteredValue.find(" ")

            for x in range(0,(gap_pos+1)):
                del tempList[0]

            oldBalance = int("".join(tempList))
            newBalance = int(amount)+oldBalance
            file.close()

            file = open(fileName, "w")
            text= toAddress+" "+str(newBalance)
            file.write("%s\n" %text)
            file.close()

        except IOError:
            file = open(fileName, 'a')
            text= toAddress+" "+str(amount)
            file.write("%s\n" %text)
            file.close()

        print "\n%s SHK sent to %s" %(amount, toAddress)
        return transact

    elif ask=="2":
        checkBalance(currentAddress)
    else:
        os._exit(1)


def genesisBlock(timestamp,nonce):
    timestamp = timestamp
    transactions = 0
    previousHash = 0
    nonce = nonce
    toHash = str(timestamp)+str(transactions)+str(previousHash)+str(nonce)
    hashDec = hashlib.sha256(toHash)
    SHA256 = hashDec.hexdigest()
    return timestamp,transactions,previousHash,SHA256,nonce



def previousHash():
    file = open('chainhashes.txt', 'r')
    lines = file.read().splitlines()
    return lines[-1]


def block(timestamp,transactions,previousHash,SHA256,nonce):
    timestamp = timestamp
    transactions = transactions
    previousHash = previousHash
    nonce = nonce
    toHash = str(timestamp)+str(transactions)+str(previousHash)+str(nonce)
    hashDec = hashlib.sha256(toHash)
    SHA256 = hashDec.hexdigest()
    return timestamp,transactions,previousHash,SHA256,nonce


def mineBlock(SHA256,difficulty,nonce):
    while SHA256[0:difficulty]!="0"*difficulty:
        nonce+=1
        blockCode = list(block(timestamp,transactions,previousHash,SHA256,nonce))
        SHA256 = blockCode[3]

    fileName = "blockchain.txt"
    file = open(fileName, 'a')
    text= str(timestamp)+str(transactions)+str(previousHash)+str(nonce)
    file.write("%s\n" %text)
    file.close()

    fileName = "chainhashes.txt"
    file = open(fileName, 'a')
    text= blockCode[3]
    file.write("%s\n" %text)
    file.close()

    print "\nBlock successfully mined:"
    print text



def checkBlockchain():
    #Check 1
    file = open("chainhashes.txt", "r")
    contents_chainHashes=[]
    for x in file:
        x = x.strip()
        x = x.strip("\n")
        x = x.strip("'")
        contents_chainHashes.append(x)

    file = open("blockchain.txt", "r")
    contents_blockchain=[]
    for x in file:
        x = x.strip()
        x = x.strip("\n")
        x = x.strip("'")
        x = hashlib.sha256(x)
        x = x.hexdigest()
        contents_blockchain.append(x)

    file.close()

    if contents_blockchain!=contents_chainHashes:
        return False

    firstChars = []

    del contents_blockchain[0]
    del contents_chainHashes[0]

    for n in range(0,len(contents_chainHashes)):
        firstChar=contents_chainHashes[n][:difficulty]
        if firstChar!="0"*difficulty:
            return False
        else:
            firstChars.append(firstChar)

    file.close()

#MAIN
difficulty = 4
runAgain = True

if checkBlockchain()==False:
    print "INVALID CHAIN"

file = open("user.txt", "r")
first=file.read(1)
second=file.read(2)
if not first or not second:
    username= ""


for enteredValue in file:
    enteredValue = enteredValue.strip()
    enteredValue = enteredValue.strip("\n")
    enteredValue = enteredValue.strip("'")
    username= enteredValue

if username=="":
    print "\nJoin Shockwave (SHK) today!"
    sleep(2)
    newUser= raw_input("Create public key: ")
    fileName = "user.txt"
    file = open(fileName, 'a')
    username= newUser
    file.write("%s\n" %username)
    file.close()
    sleep(1)


file = open("privatekey.txt", "r")

first=file.read(1)
second=file.read(2)
if not first or not second:
    key=""

for enteredValue in file:
    enteredValue = enteredValue.strip()
    enteredValue = enteredValue.strip("\n")
    enteredValue = enteredValue.strip("'")
    key= enteredValue

if key=="":
    newPass= raw_input("Create your private key: ")
    fileName = "privatekey.txt"
    file = open(fileName, 'a')
    hashDec = hashlib.sha256(newPass)
    hashedGuess = hashDec.hexdigest()
    file.write("%s\n" %hashedGuess)
    file.close()
    sleep(1)


enteredUser= raw_input("\nEnter public key: ")
file1 = open("user.txt", "r")
for enteredValue in file1:
    enteredValue = enteredValue.strip()
    enteredValue = enteredValue.strip("\n")
    enteredValue = enteredValue.strip("'")
    username = enteredValue


if enteredUser == username:
    file2 = open("privatekey.txt", "r")
    for enteredValue in file2:
        enteredValue = enteredValue.strip()
        enteredValue = enteredValue.strip("\n")
        enteredValue = enteredValue.strip("'")
        privateKey= enteredValue

    enteredPass= getpass.getpass("\nEnter private key: ")
    hashDec = hashlib.sha256(enteredPass)
    hashedGuess = hashDec.hexdigest()


    if hashedGuess == privateKey:
        while runAgain==True:
            currentAddress = username
            now = datetime.datetime.now()
            day = str(now.day)
            month = str(now.month)
            year = str(now.year)
            timestamp = day+"/"+month+"/"+year
            nonce=0
            blockCode = list(genesisBlock(timestamp,nonce))

            timestamp = timestamp
            transactions = transaction(currentAddress)

            try:
                previousHash = previousHash()
            except IndexError or TypeError:
                x = None
                previousHash=0

            SHA256 = blockCode[3]
            nonce = blockCode[4]

            mineBlock(SHA256,difficulty,nonce)
