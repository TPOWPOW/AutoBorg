#!/bin/bash

#Goal: This script will automate backing up a directory using Borgbackup

#Global variables
export BORG_REPO=root@ip:/path/to/backup
export BORG_PASSPHRASE="creds here"

#First turn on the remote server
python3 HAPowerToggle.py on || {
python3 sendMessage.py -f  "Failed to turn outlet on" && exit 1
}

#Wait 3 minutes
#UCOMMENT THIS OFF WHEN MOVING TO ACTUAL HARDWARE
sleep 300

#Next initiate the borg backup 
BORG=$(borg create --stats --show-rc --compression lz4 ::'{hostname}-{now}' /mnt/mydata 2>&1 && borg prune --list --glob-archives '{hostname}-*' --show-rc --keep-last=15 2>&1) || { 
BORG_FAIL=$'Borg script failed\nFailure Output:\n'$BORG && python3 sendMessage.py -f "$BORG_FAIL" && exit 1
}

#Next turn off the remote server
test=$(ssh root@ip "./shut" 2>&1) || {
NOBORG=$'NOTE: Backup succeeded but the server was not turned off\n'$BORG && python3 sendMessage.py -s "$NOBORG" && exit 1
}
#test=$(ssh root@192.168.1.189 "(./shut && exit)" 2>&1)
#if [[ $test != *"closed"* ]]; then
	#NOBORG=$'NOTE: Backup succeeded but the server was not turned off\n'$BORG && python3 sendMessage.py -s "$NOBORG" && exit 1
#fi

#Wait for the server to completely turn off before turning off the outlet 
sleep 180

#Next turn off the remote server outlet
python3 HAPowerToggle.py off || {
NOBORG2=$'NOTE: Backup succeeded but outlet was not turned off\n'$BORG && python3 sendMessage.py -s "$NOBORG2" && exit 1
}

#Finally send a success message via discord
python3 sendMessage.py -s "$BORG"

#Todo
#Securely code secrets
#Test APi's with wireshark to makes sure they are secure
#Rebuild Ubuntu server/plan out
#Redeploy code and test
#Set up chronjob
#Finish coding installer and making documentation in Github
