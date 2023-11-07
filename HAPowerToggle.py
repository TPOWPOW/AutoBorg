#Goal: This is a script that will turn on/off a Home Assistant outlet

from requests import get
from requests import post
import sys
import argparse

#Global variables to access the Home Assistant API
url = "http://HomeAssistant.local:8123/api/states/switch.your_switch_name_relay"
url_off = "http://HomeAssistant.local:8123/api/services/switch/turn_off"
url_on = "http://HomeAssistant.local:8123/api/services/switch/turn_on"

headers = {"Authorization": "Bearer your_API_token_here",
           "content-type": "application/json",
           }

#This function will return the status of the outlet [on, off]
def getStatus():
  response = get(url, headers=headers)
  status = str(response.json()['state'])
  return status

#This function will turn on the outlet
def turnOn():
  #First check if the outlet is already on
  currentStatus = getStatus()
  if(currentStatus == "on"):
    print("process aborted")
    return
  #If the outlet is not already on turn it on
  else:
    myobj='{"entity_id": "switch.testsonoff01_relay"}'
    response = post(url_on, headers=headers, data=myobj)
    print('Outlet is now on')
    return

#This function will turn off the outlet
def turnOff():
  #First check if the outlet is already off
  currentStatus = getStatus()
  if(currentStatus == "off"):
    print("process aborted")
    return
  else:
    myobj='{"entity_id": "switch.your_switch_entity_id"}'
    response = post(url_off, headers=headers, data=myobj)
    print('Outlet is now off')
    return


#Setting up the command line arguments
parser = argparse.ArgumentParser(description="This program will turn a Home Assistant outlet on or off")

parser.add_argument('status', choices=('on','off'), help = "choose to turn the outlet on or off")

args = parser.parse_args()


if(args.status == 'on'):
  turnOn()
else:
  turnOff()
