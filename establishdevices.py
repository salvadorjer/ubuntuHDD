#Establish devices
#devicelist may not even be needed
import os
os.system("sudo lshw -class disk -short > AttachedDevices.txt ")


listofdrives = []

def FindDrives(listofdrives):

        
    print "FindDrives gets called"
    with open("AttachedDevices.txt") as f:
        for line in f:
            if "/dev/sd" in line:
                listofdrives.append(line[29])#need line [24] USB devices as the empty spaces before /dev in the files are different line [23] for desktop and [29] for server
                print line[22:30]#this line gives us all of the drives such as: /dev/sda /dev/sdb
                #f2.write(line[23])#puts all found devices in devicelist.txt
                #####IMPORTANT do not run the first in the list for the wiping process, that is the host of the OS
                serialcommand = "serial%s.txt"%(line[29])
                serialcreate="touch serial%s.txt"%(line[29])#for some reason this seems to be the best way to create the files
                os.system(serialcreate)
                serialfile=open(serialcommand,"r+b")
                serialfile.write(line[50:70])#gets the serial numbers from the drives and writes them to the appropriate serial file

FindDrives(listofdrives)

print "Total number of drives found: ",len(listofdrives)
print listofdrives

#commented out following line leads to removing the safety of not wiping sda
print listofdrives.pop(0)#removes "a" from the list

print listofdrives

with open("devicelist.txt", 'w') as f:
    for s in listofdrives:
        f.write(s + '\n')
print "device list appended"

#####lshw doesn't list unformatted (or possibly bad?) drives. so the answer could be lsblk or ls -ltr /dev/sd*
