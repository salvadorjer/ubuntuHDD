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
                driveIdentity=line.index("/sd")+3
                print driveIdentity
                listofdrives.append(line[driveIdentity])#need line [24] USB devices as the empty spaces before /dev in the files are different line [23] for desktop and [29] for server
                print line[22:30]#this line gives us all of the drives such as: /dev/sda /dev/sdb
                #f2.write(line[23])#puts all found devices in devicelist.txt
                #####IMPORTANT do not run the first in the list for the wiping process, that is the host of the OS
                serialcommand = "serial%s.txt"%(line[driveIdentity])
                serialcreate="touch serial%s.txt"%(line[driveIdentity])#for some reason this seems to be the best way to create the files
                driveSerial=line.index("GB")+3
                os.system(serialcreate)
                serialfile=open(serialcommand,"r+b")
                serialfile.write(line[driveSerial:driveSerial+20])#gets the serial numbers from the drives and writes them to the appropriate serial file
                sizecommand="size%s.txt"%(line[driveIdentity])
                sizecreate="touch size%s.txt"%(line[driveIdentity])
                driveSize=line.index("GB")-4#this section creates sizea.txt files that contain the size of the drive with no whitespaces
                os.system(sizecreate)
                sizefile=open(sizecommand,"r+b")
                tempsize=line[driveSize:driveSize+4]
                tempsize=tempsize.lstrip(" ")
                print tempsize
                sizefile.write(tempsize)
                
                    
         

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
