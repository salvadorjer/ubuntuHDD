##Witless dragon sucessive prototype

import subprocess
import os



print "removing old files"
list = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
i=0
os.system("rm -f devicelist.txt AttachedDevices.txt")
while i <=25:#removes all files
    cleanup = "rm -f  octaldump%s.txt outputfile%s.txt blksize%s.txt" %(list[i],list[i],list[i])
    os.system(cleanup)
    i=i+1

import establishdevices
establishdevices #calls a program that will determine the number of drives
#creates the list of disks as a string in the file devicelist.txt




isClean = False #variable checking that the drive has been zeroed
IsGood = False #variable checking that the drive is finalized

def readzero (isClean,currentDrive):#function that checks the output file for zeroing the drive
    k=("outputfile%s.txt")% currentDrive
    z=open(k)
    for line in z:
        print line
        if "No space left on device" in line:
            print "all sectors allocated zero"
            return True
        else:
            print "not all sectors were zeroed"
            return False

def readcheck(isGood,currentDrive):
    k=("octaldump%s.txt")%currentDrive
    f=open(k)
    line=f.readline().strip()#strip removes the hanging new line at the end
    if line == "0000000 000000 000000 000000 000000 000000 000000 000000 000000":
        return True
    else:
        return False

def wiping(currentDrive):
    getblksize = "sudo blockdev --getbsz /dev/sd%s >> blksize%s.txt" % (currentDrive,currentDrive)
    os.system(getblksize)#get the block size for the given drive and store it in a text file
    currentblk="blksize%s.txt"%(currentDrive)
    f=open(currentblk)
    for line in f:
        bsize=line
    zero="sudo dd if=/dev/zero of=/dev/sd%s 2> outputfile%s.txt bs=%s"% (currentDrive, currentDrive, line)#puts the block size in the zeroing
    os.system(zero)
    ##most recent modification
    
    zeroingoutput=open("outputfile%s.txt"%(currentDrive))
    for check in zeroingoutput:
        if "No space left on device" in check:
            print "/dev/sd%s is filled with zeros"%(currentDrive)
    checkwipe = "sudo od /dev/sd%s >> octaldump%s.txt | head"%(currentDrive,currentDrive)
    os.system(checkwipe)#dumps the data into a file which we can then see if we find any non-zeo values
#octaldump may require further testing (unsure if terminal and file output are behaving differently)
    octaloutput=open("octaldump%s.txt"%(currentDrive))
    for check in octaloutput:
        if "0000000 000000 000000 000000 000000 000000 000000 000000 000000" in check:
            print"/dev/sd%s is fully sanitized and good to go"%(currentDrive)



########### logical start of actual program  ###########





##loop into listofdrives []
listofdrives=[]
with open('devicelist.txt', 'r') as a:
    listofdrives=a.readlines()
    print listofdrives

##loop through listofdrives[]
    ##call wiping and checking function per iteration
totaldrives =len(listofdrives)
i=0
while i<totaldrives:
    currentDrive=listofdrives[i]
    currentDrive=currentDrive.strip()
    wiping(currentDrive)

    i=i+1


