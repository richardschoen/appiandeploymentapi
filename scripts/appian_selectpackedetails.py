#------------------------------------------------
# Script name: appian_selectpackagedetails.py
#
# Description: 
# This script lists all packages for an application uuid 
# using the application uuid and returns the one that 
# is selected based on either: 
# packageuuid, packagename or packagedesc.
# It's a good example of selecting a specific package 
# by something more than needing to know the application uuid
# If you name your DevOps tickets or stories to match your 
# application package name or desc you can select a package 
# on the fly for your build rather than needing to know the
# package uuid value. The package uuid can be selected for 
# you automatically based on package name or desc.
#
# Site info is stored in the config.py file
#
# Parameters:
# --appid  - Application uuid. Get from Appian Application Properties.
# --selecttype - Type of select: packageid, packagename, packagedesc
# --selectvalue - The text string or uuid to seach for based on selecttype.
#
# Pip packages needed:
# pip install pycurl
# None - argparse is a standard module.
#------------------------------------------------
import requests
import json
import argparse
import sys
from sys import platform
import os
import re
import time
import traceback
from pathlib import Path
from datetime import date
import datetime
import pycurl
import importlib.util
from io import StringIO 
from io import BytesIO
from urllib.parse import urlencode
import config as cfgdeploy
from deployfunctions import *

# Initialize or set variables
appdesc="List and Select Application Package Details"
dashes="-------------------------------------------------------------------"
exitcode=0 #Init exitcode
exitmessage=''
httpcode=0
httpresponse=0

# Output messages to STDOUT for logging
print(dashes)
print(appdesc)
print("Start of Main Processing - " + time.strftime("%H:%M:%S"))
print("OS:" + platform)


try: # Try to perform main logic

    # Set up the command line argument parsing.
    # If the parse_args function fails, the program will
    # exit with an error 2. In Python 3.9, there is 
    # an argument to prevent an auto-exit
    # Each argument has a long and short version
    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--appid', required=True,help="Application uuid")
    parser.add_argument('-t','--selecttype', required=True,help="Select type packageuuid, packagename or packagedesc")
    parser.add_argument('-s','--selectvalue', required=True,help="Select text value or package uuid based on --selecttype")
    # Parse the command line arguments 
    args = parser.parse_args()

    # Pull arguments into variables so they are meaningful
    parmappid=args.appid.strip()
    parmselecttype=args.selecttype.strip().lower() # TO lower case
    parmselectvalue=args.selectvalue.strip()

    # Print parameters 
    print(f"Selected AppID: {parmappid}")
    print(f"SelectType: {parmselecttype}")
    print(f"SelectValue: {parmselectvalue}")

    # Make sure correct selecttype chosen
    # Otherwise bail out.
    if (parmselecttype != "packageuuid" and 
        parmselecttype != "packagename" and 
        parmselecttype != "packagedesc"):
        raise Exception("--selecttype must be:packageuuid, packagename or packagedesc")

    # Get string buffer for HTTP response
    response = BytesIO()

    # Instantiate pycurl object
    c = pycurl.Curl()

    # Set verbose mode for troubleshooting
    if (cfgdeploy.enableverbose):
       c.setopt(pycurl.VERBOSE,cfgdeploy.verbositylevel)

    # Set the Appian site deployment API url
    c.setopt(c.URL, f"{cfgdeploy.siteurl}/suite/deployment-management/v2/applications/{parmappid}/packages")

    # Set the required HTTP headers for Deployment REST API
    c.setopt(c.HTTPHEADER, [f"Appian-API-Key: {cfgdeploy.apikey}","Action-Type: export"])

    # Set post data for JSON multipart/form Deployment API call
    #c.setopt(c.HTTPPOST, [('json',datajson)])
    c.setopt(c.WRITEDATA, response)
      
    # Perform the operation and close the connection
    c.perform()
  
    # Output HTTP respone codes
    httpcode=c.getinfo(pycurl.HTTP_CODE)
    httpresponse=c.getinfo(pycurl.RESPONSE_CODE)
  
    # Close curl connection 
    c.close()

    # HTTP response code
    print("HTTP response status code: %s" % httpcode)

    # Output or fetch response data
    responsestr=response.getvalue().decode('utf-8') 
    ##print(responsestr) # DEBUG - Print RAW response data when testing
    
    # Output pretty version of JSON
    # Load JSON object
    jsonobj = json.loads(responsestr)
    # Dump prettified version to string
    json_formatted_str = json.dumps(jsonobj, indent=4)
    # Print formatted JSON string
    print(json_formatted_str) # DEBUG - Print formatted JSON when testing
    
    # Iterate JSON result object and print each package uuid. 
    # You can change this as needed for your requirements
    print(f"Package Information for App: {parmappid}")
    for item in jsonobj['packages']:
        print(dashes) 
        #print(f"uuid:{item['uuid']},Name:{item['name']}")
        print(f"Package name: {item['name']}")
        print(f"Package desc: {item['description']}")
        print(f"Package uuid: {item['uuid']}")
        print(f"Created:{item['createdTimestamp']}")
        print(f"Updated:{item['lastModifiedTimestamp']}")
        print(f"Ticket link:{item['ticketLink']}")
        
    # Iterate JSON result object and print each selected 
    # package uuid and information based on selecttype and 
    # selectvalue parameters.
    # You can change this as needed for your requirements
    selected=False
    for item in jsonobj['packages']:
         
        # Determine if we have the right package 
        if (parmselecttype=="packageuuid" and item['uuid']==parmselectvalue): 
           selected = True
        if (parmselecttype=="packagename" and item['name']==parmselectvalue): 
           selected = True
        if (parmselecttype=="packagedesc" and item['description']==parmselectvalue): 
           selected = True
        
        # If package was selected list it.
        if (selected==True):   
          print(f"Selected Package Information for App: {parmappid}")
          print(dashes) 
          #print(f"uuid:{item['uuid']},Name:{item['name']}")
          print(f"Selected Package name: {item['name']}")
          print(f"Selected Package desc: {item['description']}")
          print(f"Selected Package uuid: {item['uuid']}")
          print(f"Created:{item['createdTimestamp']}")
          print(f"Updated:{item['lastModifiedTimestamp']}")
          print(f"Ticket link:{item['ticketLink']}")

    # Close response buffer
    response.close()

    # Set success info
    exitcode=0
    exitmessage=f"{appdesc} completed successfully."

#------------------------------------------------
# Handle Exceptions
#------------------------------------------------
# System Exit occurred. Most likely from argument parser
# We will just set the exist code and return message info.
except SystemExit as ex:
     exitcode=ex.code # set return code for stdout
     exitmessage=f"Command line argument error:{str(ex)}" # set exit message for stdout

except argparse.ArgumentError as exc:
     exitcode=99 # set return code for stdout
     exitmessage=str(exc) # set exit message for stdout
     print('Traceback Info') # output traceback info for stdout
     traceback.print_exc()      
     sys.exit(99)

except Exception as ex: # Catch and handle exceptions
     exitcode=99 # set return code for stdout
     exitmessage=str(ex) # set exit message for stdout
     print('Traceback Info') # output traceback info for stdout
     traceback.print_exc()        
     sys.exit(99)
#------------------------------------------------
# Always perform final processing
#------------------------------------------------
finally: # Final processing
     # Do any final code and exit now
     # We log as much relevent info to STDOUT as needed
     print("")
     print(dashes)
     print('ExitCode:' + str(exitcode))
     print('ExitMessage:' + exitmessage)
     print("End of Main Processing - " + time.strftime("%H:%M:%S"))
     print(dashes)

