#!/usr/bin/python
# ‐*‐ coding: utf‐8 ‐*‐
#Will Assad

import hashlib
import datetime
import smtplib
import imaplib
import fixissue
import random
import encryption
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from time import sleep
import getpass
import sys
import os

'''

The following is a secure encoded cryptocurrency using a private blockchain.
It involves electronic transfer by email of SHK (money).
Copyright © Will Assad 2018
Python 2.7

'''

#Questions: willassadcode@gmail.com

''' BLOCKCHAIN FUNCTIONS:
    Functions that operate the cryptocurrency.
    Transaction related functions at the first half,
    Cryptographic functions at the second half.
'''

def checkBalance(currentAddress): #purpose: checks the balance of the current address
    print "\nWaiting for miner..."
    
    whichUser = currentAddress
    fileName = whichUser+".txt" #if user address is "bob" then the filename is "bob.txt"
    setPath = "/"+whichUser+"/"+fileName #path depends on user account
    path = os.getcwd()+setPath    
    #fileName used to track how much money a specific user has
    
    try: #attempt to open file to check balance of user
        
        file = open(path, "r") #open the account file depending on user
        for enteredValue in file: #strip for formatting
            enteredValue = enteredValue.strip()
            enteredValue = enteredValue.strip("\n")
            enteredValue = enteredValue.strip("'")

        tempList = list(enteredValue)
        gap_pos = enteredValue.find(" ") #find gap position in text

        for x in range(0,(gap_pos+1)): #stored i.e. "Bob 18" means that Bob has 18 SH
            del tempList[0] #remove user and keep balance

        balance = int("".join(tempList))
        print "\nYour current balance is %s SHK" %(balance)
        return balance
        
    except IOError: #account file cannot be found, thus user has no balance
        print "\nNo current balance. Buy SHK on coinbase."
        balance = 0
        return balance


def confirmTransaction(amount,toAddress): #purpose: confirm that user wants to send money
    print "\nAre you sure you want to send %s SHK to %s?" %(amount,toAddress)
    print "Enter YES to confirm, any other key to abort."
    abort = (raw_input("> ")).upper()
    
    if abort=="YES" or abort=="Y":
        return True
    else:
        return False

def sendMoney(currentAddress,email,unm,pwd): #purpose: send money to another person (SHK)
    fromAddress = currentAddress

    while True:
        toEmail = raw_input("\nSend to (email): ") #find email address of who to send the email to
        toAddress = list(toEmail) #convert to list
        
        try: #check if email is entered by finding "@"
            index_at = toAddress.index("@")
            toAdd = []
            #email formatting: i.e. bob123@gmail.com
            #remove @gmail.com by tracking "@"
            for r in range(0,index_at):
                toAdd.append(toAddress[r])
            
            #store address of receiver by removing "@gmail.com"
            toAddress = ''.join(str(n) for n in toAdd)
            
            if fromAddress == toAddress: #if the user is trying to send money to themself
                sleep(3)
                print("Transaction cannot be completed: ") 
                break
                
            amount = raw_input("Amount: ") #input as string to check if number
            numbers= ["1","2","3","4","5","6","7","8","9","0"]
            for x in amount: 
                if x not in numbers: #if user enters a value that is not a number
                    print "Transaction cannot be completed: "
                    stop = True
                else:
                    stop = False
                
                if stop ==True:
                    break
                
            amount = int(amount)
            
            if amount <= 0: #if the user enters an amount to send less than or equal to 0
                sleep(2)
                print("Transaction cannot be completed.")
                break
            
            if confirmTransaction(amount,toAddress) == False: #if user does not want to execute transaction
                break
            
            print "\nWaiting for miner..."
            
            #LEDGER: store transaction history of who is sending and receiving SHK
            setPath = "/Blockchain/transactionhistory.txt"
            path_transaction = os.getcwd()+setPath #specific path in subfolder "Blockchain"
            file = open(path_transaction, "a")
            text = str(fromAddress)+str(toAddress)+str(amount) #append to the blockchain
            file.write("%s\n" %text)
            file.close()
        
        
            #WRITING BALANCE OF SENDER: subtract balance that has been sent from the sender
            fileName = fromAddress+".txt" 
            try: #check if user has an account stored on text file
                setPath = "/"+fromAddress+"/"+fileName #set specific path depending on sender
                path = os.getcwd()+setPath             
                file = open(path, "r")
                for enteredValue in file: #strip for formatting
                    enteredValue = enteredValue.strip()
                    enteredValue = enteredValue.strip("\n")
                    enteredValue = enteredValue.strip("'")
        
                tempList = list(enteredValue)
                gap_pos = enteredValue.find(" ") #find gap position to remove name store balance
        
                for x in range(0,(gap_pos+1)): #deletes name of user i.e delete "Bob " from "Bob 14"
                    del tempList[0]
        
                oldBalance = int("".join(tempList)) #old balance is currently stored on file
        
                if int(amount)>oldBalance: #if the user wants to send money greater than current balance
                    print "Insufficient funds."
                    break
        
                newBalance = oldBalance - int(amount) #update balance
                file.close()
                
                file = open(path, "w")
                text= fromAddress+" "+str(newBalance)
                file.write("%s\n" %text) #write the new balance on the text file
                file.close()
        
                transact = str(fromAddress)+str(toAddress)+str(amount) #create transaction data to hash into block
        
            except IOError: #if user has no account
                print "Insufficient funds."
                break
        
                
            #TRANSACTION BETWEEN ANOTHER NODE: give access code to deposit money to another node
            setPath = "/"+toAddress+"/"+toAddress+"_moneypass.txt"
            path = os.getcwd()+setPath      
            try:
                file = open(path,"a")
            except IOError:
                os.makedirs(toAddress)
                file = open(path,"w")
            code = []
            appendents = list("1234567890qwertyuiopasdfghjklzxcvbnm")
            for x in range(0,8): #generate a random access code
                code.append(random.choice(appendents))
            
            code = ''.join(str(n) for n in code)
            code = code + str(amount)
            hashDec = hashlib.sha256(code)
            hashedCode = hashDec.hexdigest() #hash the code to prevent hack
            
            file.write("%s\n" %hashedCode) #write the hashed code to file
            file.close()
            
            #email code to receiver
            sa = email #reformat of variables: kind of useless, but makes sense
            ta = toEmail
            body = "Received %s SHK. Access by using code: %s" %(amount,code)
            unm = unm #remember which variables when coding
            pwd = pwd
            
            msg = MIMEMultipart()
            msg['From'] = sa #message from
            msg['To'] = ta #message to
            msg['subject'] = "Transaction in SHK" #subject line
            msg.attach(MIMEText(body))
            
            srvr = smtplib.SMTP('SMTP.gmail.com:587') #send through gmail for now
            
            #send email
            srvr.ehlo()
            srvr.starttls()
            srvr.ehlo()
            srvr.login(unm,pwd)
            srvr.sendmail(sa,ta,msg.as_string())
            srvr.quit()     
        
            
            print "\n%s SHK sent to %s" %(amount, toAddress)
            return transact #return transaction code to be hashed into block            
        
        except: #if email is not entered
            print "Either an invalid email address was entered, or another issue occured." 
            print "Try to enter email again, if issue still occurs run \"fixIssue.py\"."


def depositMoney(currentAddress): #purpose: deposit money
    fromAddress = currentAddress
    key_guess = raw_input("\nEnter deposit key: ")
    keyGuess = list(key_guess)
    hashDec = hashlib.sha256(key_guess)
    hashedGuess = hashDec.hexdigest() #hash the users guess of the deposit key 
    
    print "\nWaiting for miner..."
    
    try: #check if user has an access code
        fileName = fromAddress+"_moneypass.txt"
        setPath = "/"+username+"/"+fileName
        path = os.getcwd()+setPath        
        file = open(path,"r") #read the money pass file for hashed code
        
        hash_passes = [] 
        for x in file:
            x = x.strip()
            x = x.strip("\n")
            x = x.strip("'")
            hash_passes.append(x) #add all previously hashed codes to list
        file.close()
        
        if hashedGuess in hash_passes: #if the user enters a correct deposit key
            hash_location = hash_passes.index(hashedGuess) #find where key is
            
            for z in range(0,8):
                del keyGuess[0]
            amountReceived = ''.join(str(n) for n in keyGuess) #find the amount of money from key
            
            try: #check if user has an account stored on text file
                fileName = currentAddress + ".txt"
                setPath = "/"+username+"/"+fileName
                path = os.getcwd()+setPath                
                file = open(path, "r")
                for enteredValue in file: #strip for formatting
                    enteredValue = enteredValue.strip()
                    enteredValue = enteredValue.strip("\n")
                    enteredValue = enteredValue.strip("'")
        
                tempList = list(enteredValue)
                gap_pos = enteredValue.find(" ") #find gap position to remove name store balance
        
                for x in range(0,(gap_pos+1)): #deletes name of user i.e delete "Bob " from "Bob 14"
                    del tempList[0]
        
                oldBalance = int("".join(tempList)) #old balance is currently stored on file
                file.close()
                
                newBalance = oldBalance + int(amountReceived)
                
                fileName = currentAddress + ".txt"
                setPath = "/"+username+"/"+fileName
                path = os.getcwd()+setPath                 
                file = open(path, "w")
                text= fromAddress+" "+str(newBalance)
                file.write("%s\n" %text) #write the new balance on the text file
                file.close()
        
            except IOError: #if user has no account
                fileName = currentAddress + ".txt"
                setPath = "/"+username+"/"+fileName
                path = os.getcwd()+setPath                 
                file = open(path, "w")
                text = fromAddress+" "+amountReceived
                file.write("%s\n" %text) #write the new balance on the text file
                file.close()
            
            del hash_passes[hash_location] #delete code as balance is delivered
            hash_passes.insert(hash_location, "None") #insert "None"
            
            fileName = fromAddress+"_moneypass.txt"
            setPath = "/"+username+"/"+fileName
            path = os.getcwd()+setPath
            file = open(path,"w") #clear old deposit codes
            for q in range(0,len(hash_passes)):
                file.write("%s\n" %hash_passes[q]) #write updated hashed codes
            file.close()
            return amountReceived
        
        else: #if user enters an invalid deposit code
            print "\nInvalid deposit code."
            amountReceived = "0"
            return amountReceived
        
    except IOError: #if user has no access code
        print "No Money Has Been Sent."   
        amountReceived = "0"
        return amountReceived


def exit(this):
    try:
        if this==True:
            return "break"
    except:
        return "nobreak"

def transaction(): #main function, purpose: send money, deposit money
    ask=raw_input("\n1. Send Money \n2. Deposit \n3. View Balance \n4. Quit \n> ")
    
    if ask=="1": #if user chooises to send money to someone else
        return sendMoney(currentAddress,email,unm,pwd)
    
    elif ask =="2": #if user wants to deposit money
        depositMoney(currentAddress)
    
    elif ask=="3": #if user chooses to check their balance
        checkBalance(currentAddress)
        
    elif ask == "4": #if user chooses to quit
        this = True
        return exit(this)
    
    else: #if user enters a command other than 1, 2, 3, or 4
        print "Command Not Recognized"

def genesisBlock(timestamp,nonce): #purpose: initiate the blockchain with the genesis block
    timestamp = timestamp
    transactions = 0
    
    try:
        setPath = "/Blockchain/chainhashes.txt"
        path_chainhashes = os.getcwd()+setPath #previous hash located in subfolder  
        file = open(path_chainhashes, 'r')
        lines = file.read().splitlines()
        previousHash = lines[-1]
        file.close()
    except TypeError: #if there is no previous hash
        previousHash=0  
    
    nonce = nonce
    toHash = str(timestamp)+str(transactions)+str(previousHash)+str(nonce) #hash the variables
    hashDec = hashlib.sha256(toHash)
    SHA256 = hashDec.hexdigest()
    return timestamp,transactions,previousHash,SHA256,nonce


def previousHash(): #purpose: find the hash of the last block
    setPath = "/Blockchain/chainhashes.txt"
    path_chainhashes = os.getcwd()+setPath #previous hash located in subfolder  
    file = open(path_chainhashes, 'r')
    lines = file.read().splitlines()
    return lines[-1]

def block(timestamp,transactions,previousHash,SHA256,nonce): #purpose: new block on the blockchain
    setPath = "/Blockchain/chainhashes.txt"
    path_chainhashes = os.getcwd()+setPath #previous hash located in subfolder  
    file = open(path_chainhashes, 'r')
    lines = file.read().splitlines()  
    previousHash = lines[-1]
    
    toHash = str(timestamp)+str(transactions)+str(previousHash)+str(nonce) #hashes variables
    hashDec = hashlib.sha256(toHash)
    SHA256 = hashDec.hexdigest()
    return timestamp,transactions,previousHash,SHA256,nonce


def mineBlock(SHA256,difficulty,nonce): #mine a block to add to the blockchain
    while SHA256[0:difficulty]!="0"*difficulty: #proof of work algorithm based off of the difficulty
        nonce+=1 #change the nonce until the hash has the correct number of 0s
        blockCode = list(block(timestamp,transactions,previousHash,SHA256,nonce))
        SHA256 = blockCode[3]

    setPath = "/Blockchain/blockchain.txt"
    path_blockchain = os.getcwd()+setPath    
    file = open(path_blockchain, 'a') #update blockchain
    
    text = str(timestamp)+str(transactions)+blockCode[2]+str(nonce) #update the blockchain (append only)
    file.write("%s\n" %text)
    file.close()
    
    setPath = "/Blockchain/chainhashes.txt"
    path_chainhashes = os.getcwd()+setPath
    file = open(path_chainhashes, 'a')  #add all hashes to a file
    text = blockCode[3]
    file.write("%s\n" %text)
    file.close()

    print "\nBlock successfully mined:"
    print text



def checkBlockchain(): #purpose: verify that the blockchain is not corrupt
    #Check 1: Do other copies of the blockchain match?
    setPath = "/Blockchain/chainhashes.txt"
    path_chainhashes = os.getcwd()+setPath    
    file = open(path_chainhashes, "r") #open copy of the hashes
    contents_chainHashes=[]
    for x in file: #add to list
        x = x.strip()
        x = x.strip("\n")
        x = x.strip("'")
        contents_chainHashes.append(x)
    file.close()
    
    setPath = "/Blockchain/blockchain.txt"
    path_blockchain = os.getcwd()+setPath    
    file = open(path_blockchain, "r") #open copy of the blockchain
    contents_blockchain=[]
    for x in file:
        x = x.strip()
        x = x.strip("\n")
        x = x.strip("'")
        x = hashlib.sha256(x)
        x = x.hexdigest() #hash the each line
        contents_blockchain.append(x) #add to list

    file.close()

    if contents_blockchain!=contents_chainHashes: #make sure the contents are equal
        return False
    
    #Check 2: make sure the hashes have the correct number of 0s corresponding to difficulty
    firstChars = []

    del contents_blockchain[0] #genesis block "hello" is test, delete as hash is incorrect
    del contents_chainHashes[0]

    for n in range(0,len(contents_chainHashes)): #first x amount of characters should be 0s
        firstChar=contents_chainHashes[n][:difficulty]
        if firstChar!="0"*difficulty:
            return False
        else:
            firstChars.append(firstChar)

    file.close()




#Questions: willassadcode@gmail.com

'''MAIN CODE:
   Code that calls upon the blockchain functions
   Includes login and register
'''

if __name__ == "__main__":
    difficulty = 4 #set difficulty to 4
    giftAmount = 15
    runAgain = True
    
    if checkBlockchain()==False: #if the blockchain is invalid, shut down
        print "\nINVALID BLOCKCHAIN: corruption detected."
        execute = False
    else:
        execute = True
    
    
    while execute == True:
        log_reg = (raw_input("\nType LOGIN to login, type REGISTER to register, \ntype QUIT to quit, or type ISSUE to fix an issue.\n> ")).upper()
        
        if log_reg == "LOGIN" or log_reg == "L": #if user wants to login to their account
            
            accounts = {} #create a dictionary with key of the username and value of the hashed password
            with open("accounts.txt") as f:
                for line in f:
                    (key, val) = line.split()
                    accounts[str(key)] = val #add to dictionary of accounts
                    
            user_guess = raw_input("\nEnter username: ") #ask user to enter username
            
            if user_guess in accounts: #verify that the username is stored on file
                username = user_guess
                hashedPassword = accounts.get(username) #find the corresponing password
                password_guess = raw_input("Enter password: ")
                hashDec = hashlib.sha256(password_guess)
                hashedGuess = hashDec.hexdigest() #hash their guess of the password
                
                if hashedGuess == hashedPassword: #if the user enters the correct password
                    currentAddress = username
                    fileName = currentAddress + "_emailUser.txt" #find their email user
                    setPath = "/"+username+"/"+fileName
                    path = os.getcwd()+setPath                 
                    file = open(path,"r")
                    for enteredValue in file:
                        enteredValue.strip()
                        enteredValue.strip("\n")
                        enteredValue.strip("'")
                        unm = enteredValue #email username from file
                    
                    email = unm + "@gmail.com" #generate email based off of username
                    file.close()
                    
                    fileName = currentAddress + "_emailPass.txt" #find their email password
                    setPath = "/"+username+"/"+fileName
                    path = os.getcwd()+setPath                
                    file = open(path,"r")
                    pwd = []
                    for enteredValue in file: #strip for formatting
                        enteredValue = enteredValue.strip()
                        enteredValue = enteredValue.strip("\n")
                        enteredValue = enteredValue.strip("'")
                        pwd.append(enteredValue) #take encrypted text and append to list
                    
                    del pwd[0] #delete blank
                    pwd = map(int, pwd) #change list of encrypted strings to list of encrypted integers
                    
                    pwd = encryption.wordDecrypt(pwd) #decrypt the integers to plain text of email password
                    file.close()            
                    
                    '''THIS IS THE MAIN PART OF THE CODE ONCE ACCOUNT IS SET UP
                       USER CAN NOW SEND, DEPOSIT, AND VIEW BALANCE
                    '''
                    while runAgain==True: #while user wants to execute another task
                        #necessary variables for blockchain:
                        currentAddress = username
                        now = datetime.datetime.now()
                        day = str(now.day)
                        month = str(now.month)
                        year = str(now.year)
                        timestamp = day+"/"+month+"/"+year
                        nonce = 0
                        blockCode = list(genesisBlock(timestamp,nonce))
            
                        timestamp = timestamp
                        transactions = transaction()
                        
                        if transactions == "break":
                            break
            
                        try: #attempt to check previous hash
                            previousHash = previousHash()
                            #previousHash()
                        except TypeError: #if there is not previous hash
                            x = None
                            previousHash=0
            
                        #if previousHash!=0: #if the previous hash exists
                            #previousHash = previousHash()
            
                        SHA256 = blockCode[3] #find hash from blockcode
                        nonce = blockCode[4] #find nonce from blockcode
            
                        mineBlock(SHA256,difficulty,nonce) #mine block to chain            
                else:
                    print "\nIncorrect Password"
            else:
                print "\nUser Does Not Exist."
        
        
        elif log_reg == "REGISTER" or log_reg == "R": #if user chooses to register new account
            
            '''
               GENESIS BLOCK???
            '''
            print "\nWelcome to SHK (Shockwave)."
            sleep(3)
            print "I will guide you through making an account."
            sleep(3)
            accounts = {} #create a dictionary with key of the username and value of the hashed password
            with open("accounts.txt") as f:
                for line in f:
                    (key, val) = line.split()
                    accounts[str(key)] = val #add to dictionary of accounts        
            while True:
                username = raw_input("\nEnter a new username: ")
                if username in accounts:
                    print "User Already Exists."
                else:
                    break
                
            pass_plainText = raw_input("Enter a new password: ")
            hashDec = hashlib.sha256(pass_plainText)
            hashedPassword = hashDec.hexdigest() #hash the plain text password
            file = open("accounts.txt","a") 
            text = username + " " + hashedPassword #add the username and password to file
            file.write("\n%s" %text)
            file.close()
            
            currentAddress = username
            
            emailAddress = list(raw_input("Enter (gmail) email: "))
            atLocation = emailAddress.index("@")
            
            unm = []
            for x in range(0,atLocation): #from entered username take text up to "@" sign
                unm.append(emailAddress[0])
                del emailAddress[0]
            
            emailServer = ''.join(str(n) for n in emailAddress) 
            unm = ''.join(str(n) for n in unm)
            
            if emailServer != "@gmail.com": #email only supports gmail for now, will change later
                print "Email server not supported: "
                break
            
            os.makedirs(username) #make new directory for the users files
            fileName = currentAddress+"_emailUser.txt"
            setPath = "/"+username+"/"+fileName
            path = os.getcwd()+setPath
            file = open(path,"w") #add the email username to text file
            file.write(unm)
            file.close()
            
            email = unm + emailServer
            
            fileName = currentAddress + "_emailPass.txt"
            setPath = "/"+username+"/"+fileName
            path = os.getcwd()+setPath        
            pwd = encryption.wordEncrypt(raw_input("Enter email password for \"%s\": " %(email))) #encrypt plain text password
            file = open(path,"w")
            for x in range(0,len(pwd)):
                file.write("\n%s"%pwd[x]) #write encrypted password to file
            file.close()
            
            
            print "\nCongradgulations %s! Your account has now been created." %(username)
            sleep(2)
            if giftAmount != 0:
                print "You have been gifted %s SHK to play with." %(giftAmount)
            fileName = currentAddress + ".txt"
            setPath = "/"+username+"/"+fileName
            path = os.getcwd()+setPath 
            file = open(path,"w")
            text = currentAddress + " " + str(giftAmount)
            file.write(text)
            file.close()        
        
        
        elif log_reg=="QUIT" or log_reg=="Q":
            print "\nThank you."
            break
        
        elif log_reg=="ISSUE" or log_reg=="I":
            print "\nPossible Issues: "
            fixissue.main()
            break
        else:
            print "\nCommand Not Recognized."