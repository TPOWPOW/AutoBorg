#Goal: This is the second version of the sendMessage script, used to send alerts via a Discord bot using webhooks

import sys
from discord import SyncWebhook
import argparse
from datetime import date
from datetime import datetime
#Discord Webhook URL
webhook = SyncWebhook.from_url("Discord webhook here")

#Print out the date and time

def dateandtime():
  now = datetime.now()
  current_date = date.today()
  formatted_date1 = current_date.strftime("%d-%b-%Y")
  current_time = now.strftime("%H:%M:%S")
  time = "Date: " + formatted_date1 + "\nTime: " + current_time
  return time


#Send a message to signal a successful backup
def sendSuccess(message):
  message = "\n" + dateandtime() + "\n" + message 
  webhook.send("BACKUP SUCCEEDED \nAdditional Information:" + message+'\n')    

#Send a message to signal a unsuccessful backup
def sendFailure(message):
  message = "\n" + dateandtime() + "\nFailure Reason: " + message 
  webhook.send("BACKUP FAILED \nAdditional Information:" + message+'\n')

parser = argparse.ArgumentParser(description='This program is designed to send a message from a Discord bot')

parser.add_argument('-s', '--success',action='store_true',help='send a success notification')

parser.add_argument('-f', '--fail',action='store_true',help='send a failure notification')

parser.add_argument('message',type=str,help='send a message')

args = parser.parse_args()

message = args.message

if(args.fail == True and args.success == True):
  raise argparse.ArgumentTypeError(f'These are mutually exclusive only 1 may be used at a time')
elif(args.fail == False and args.success == False):
  raise argparse.ArgumentTypeError(f'the following arguments are required: -s or -f')
elif(args.fail == True):
  sendFailure(message)
else:
  sendSuccess(message)
