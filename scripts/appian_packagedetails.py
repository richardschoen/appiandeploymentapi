#------------------------------------------------
# Script name: appian_packagedetails.py
#
# Description: 
# This script lists all packages for an application uuid 
# using the application uuid.
#
# Site info is stored in the config.py file
#
# Parameters:
# --appid  - Application uuid. Get from Appian Application Properties.
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
appdesc="List Application Package Details"
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
    # Parse the command line arguments 
    args = parser.parse_args()

    # Pull arguments into variables so they are meaningful
    parmappid=args.appid.strip()

    # Get tring buffer for HTTP response
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
    ## print(json_formatted_str) # DEBUG - Print formatted JSON when testing
    
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

    # Close response buffer
    response.close()

    # Set success info
    exitcode=0
    exitmessage=f"{appdesc} completed successfully."

#------------------------------------------------
# Handle Exceptions
#------------------------------------------------
# System Exit occurred. Most likely from argument parser
except SystemExit as ex:
     ### print("Command line argument error.")
     ### Set exitcode and exitmessage message for stdout. 
     ### Ex comes back as same value as ex.code from argparse SystemExit
     exitcode=ex.code # set return code for stdout
     exitmessage=f"Command line argument error:{str(ex)}" # set exit message for stdout
     ###Enable the following for detailed trace
     ###print('Traceback Info') # output traceback info for stdout
     ###traceback.print_exc()      

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

