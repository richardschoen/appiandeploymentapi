#------------------------------------------------
# Script name: appian_exportpackage.py
#
# Description: 
# This script starts a package deployment. 
# using an application package uuid.
# It will download the ZIP package file and log file 
# when the deployment is complete.
#
# **Enhancement notes: 
# This script currently only supports downloading the 
# package ZIP file. It could be enhanced to download the 
# other files as well.  
#
# Site info is stored in the config.py file
#
# Parameters:
# --packageid  - Application package uuid. Get from Appian package details
#                via the appian_packagedetails.py script. 
#
# Pip packages needed:
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
import threading
import traceback
from pathlib import Path
from datetime import date
import datetime
import pycurl
from io import StringIO 
from io import BytesIO
from urllib.parse import urlencode
import config as cfgdeploy
from deployfunctions import *

# Initialize or set variables
appdesc="Export Package"
dashes="-------------------------------------------------------------------"
exitcode=0 #Init exitcode
exitmessage=''

# Output messages to STDOUT for logging
print(appdesc)
print(dashes)
print("Start of Main Processing - " + time.strftime("%H:%M:%S"))
print("OS:" + platform)

try: # Try to perform main logic

    # Set up the command line argument parsing.
    # If the parse_args function fails, the program will
    # exit with an error 2. In Python 3.9, there is 
    # an argument to prevent an auto-exit
    # Each argument has a long and short version
    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--packageid', required=True,help="Application package uuid")
    parser.add_argument('-n','--deploymentname', required=True,help="Application package deployment name")
    parser.add_argument('-d','--deploymentdesc', required=True,help="Application package deployment desc")
    parser.add_argument('-z','--outputzipfile', required=True,help="Output zip package file")
    parser.add_argument('-l','--outputlogfile', required=True,help="Output log file file")
    parser.add_argument('-r','--replace',default="False",required=False,help="True=Replace output file,False=Do not replace output file. Default=False")
    # Parse the command line arguments 
    args = parser.parse_args()

    # Pull arguments into variables so they are meaningful
    parmapppackageid=args.packageid.strip()
    parmdeploymentname=args.deploymentname.strip()
    parmdeploymentdesc=args.deploymentdesc.strip()
    parmoutputzipfile=args.outputzipfile.strip()
    parmoutputlogfile=args.outputlogfile.strip()
    parmreplace=str2bool(args.replace.strip())

    # If file names have any template info, replace into file names
    # @@datetime = replace timestamp - yyyymmddhhmmss in file name
    # @@appid = replace application id in file name
    # @@packageid = replace package id in file name
    parmoutputzipfile=format_file_name(parmoutputzipfile,appid=parmapppackageid)
    print(f"Output packageZip file: {parmoutputzipfile}")
    parmoutputlogfile=format_file_name(parmoutputlogfile,appid=parmapppackageid)
    print(f"Output log file: {parmoutputlogfile}")

    # Check for output ZIP file 
    if (os.path.exists(parmoutputzipfile)):
        # Kill file if replace. Otherwise throw exists error 
        if (parmreplace): 
            os.remove(parmoutputzipfile)   
        else:
            raise Exception(f"File {parmoutputzipfile} exists and --replace=True was not selected. Process cancelled.")     

    # Check for output LOG file 
    if (os.path.exists(parmoutputlogfile)):
        # Kill file if replace. Otherwise throw exists error 
        if (parmreplace): 
            os.remove(parmoutputlogfile)   
        else:
            raise Exception(f"File {parmoutputlogfile} exists and --replace=True was not selected. Process cancelled.")     

    # Set up JSON field for post to Appian REST Deployment API
    datajson="{" + f"\"name\":\"{parmdeploymentname}\",\"description\":\"{parmdeploymentdesc}\",\"uuids\":[\"{parmapppackageid}\"],\"exportType\":\"package\"" + "}"

    # Create post data array
    post_data = [('json',datajson)]

    # Get string buffer for HTTP response
    response = BytesIO()

    # Instantiate pycurl object
    c = pycurl.Curl()

    # Set verbose mode for troubleshooting
    if (cfgdeploy.enableverbose):
       c.setopt(pycurl.VERBOSE,cfgdeploy.verbositylevel)

    # Set the Appian site deployment API url
    c.setopt(c.URL, f"{cfgdeploy.siteurl}/suite/deployment-management/v2/deployments")

    # Set the required HTTP headers for Deployment REST API
    c.setopt(c.HTTPHEADER, [f"Appian-API-Key: {cfgdeploy.apikey}","Action-Type: export"])

    # Set post data for JSON multipart/form Deployment API call
    c.setopt(c.HTTPPOST, [('json',datajson)])
    c.setopt(c.WRITEDATA, response)
    
    # Perform the post and close the connection
    c.perform()
    c.close()

    # Output or fetch response data
    #print (response.getvalue())
    responsestr=response.getvalue().decode('utf-8') 
    
    # Output pretty version of JSON
    # Load JSON object
    jsonobj = json.loads(responsestr)
    # Dump prettified version to string
    json_formatted_str = json.dumps(jsonobj, indent=4)
    # Print formatted JSON string
    print(json_formatted_str)

    # Close response buffer
    response.close()

    # Print each package uuid. You can change as needed for your requirements
    print(f"Export Information for App Package: {parmapppackageid}")
    print(dashes)
    print(f"Package export uuid: {jsonobj['uuid']}")
    print(f"Package export url: {jsonobj['url']}")
    print(f"Package export status: {jsonobj['status']}")
    # Save export status so we can loop to monitor export progress
    exportuuid=f"{jsonobj['uuid']}"
    exporturl=f"{jsonobj['url']}"
    exportstatus=f"{jsonobj['status']}"
        
    # Loop to monitor for export progress using deployment check URL
    deployDone=False # Reset deploy complote flag
    deployCheckMax=10 # Max iterations
    deploySleepSeconds=5 # Slee xx seconds between checks
    deployStatusDebug=True # Pring debug info for check_deployment_status
    currentDeployCheck=0 # Current check counter
    currentDeployStatus="" # Current check deployment status result
    currentDeployJson="" # Current check deployment status result JSON

    while deployDone==False and currentDeployCheck < deployCheckMax: 
          # If deployment still in progress, wait 5 seconds and recheck
          currentDeployStatus=check_deployment_status(exporturl,deployStatusDebug)
          if currentDeployStatus=="IN_PROGRESS":
             print(f"Deployment is still in progress. Waiting for {deploySleepSeconds} seconds...")  
             time.sleep(5)                
          else:
             # Deployment must have completed on last check  
             deployDone=True 
             # Increment the current deployment iteration counter
             currentDeployCheck +=1

    print(f"Deployment is done with status: {currentDeployStatus}")
 
    # Get deployment status JSON
    currentDeployJson=check_deployment_status_json(exporturl,False)
   
    print(dashes)
    print("Deployment Results")
    print(f"packageZip: {currentDeployJson['packageZip']}")
    print("")
    print(f"deploymentLogUrl: {currentDeployJson['deploymentLogUrl']}")
    print("")
    print(f"status: {currentDeployJson['status']}")
    
    # Download completed application export files here. Always replace
    print(dashes)
    donezip=download_deployment_results(currentDeployJson['packageZip'],parmoutputzipfile,True,True)
    print(f"Zip package file downloaded to: {parmoutputzipfile}, Success:{donezip}")
    
    print(dashes)
    donelog=download_deployment_results(currentDeployJson['deploymentLogUrl'],parmoutputlogfile,True,True)
    print(f"Deployment log file downloaded to: {parmoutputlogfile}, Success:{donelog}")

    # Set success info
    exitcode=0
    exitmessage=f"{appdesc} completed successfully."

#------------------------------------------------
# Handle Exceptions
#------------------------------------------------
# System Exit occurred. Most likely from argument parser
# We will just set the exit code and return message info.
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
