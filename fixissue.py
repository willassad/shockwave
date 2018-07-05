from time import sleep
import os

def invalidChain():
    setPath = "/Blockchain/chainhashes.txt"
    path_chainhashes = os.getcwd()+setPath
    file = open(path_chainhashes, "w")  #add all hashes to a file
    file.write("2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824\n")
    file.close()
    
    setPath = "/Blockchain/blockchain.txt"
    path_chainhashes = os.getcwd()+setPath
    file = open(path_chainhashes, "w")  #add all hashes to a file
    file.write("hello\n")
    file.close()
    
    print "\nBlockchain Reset. Check if issue fixed."

def transactionError():
    print "\nThis is most likely an issue with email login."
    sleep(3)
    print "First check internet connection. Transactions cannot occur without this."
    sleep(3)
    print "\nIf it still doesn't work, register a new account."
    sleep(3)
    print "Make sure you enter email username and password correctly."
    sleep(4)
    print "\nIf this does not fix the issue, contact me: willassadcode@gmail.com"    


def main():
    while True:
        print "\n1. Invalid Chain"
        print "2. Transaction Not Sending"
        print "3. Other Issue"
        problem = raw_input("> ")    
        
        if problem == "1":
            print "\nYou are having an invalid chain issue."
            sleep(2)
            print "Attempting to fixing issue..."
            invalidChain()
            break
        
        elif problem == "2":
            print "\nYou are having an issue with transactions."
            sleep(3)
            transactionError()
            break
        
        elif problem == "3":
            print "\nEmail willassadcode@gmail.com and describe your issue."
            break
        
        else:
            print "Command Not Recognized."