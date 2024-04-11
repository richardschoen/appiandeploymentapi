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
import importlib.util
from io import StringIO 
from io import BytesIO
from urllib.parse import urlencode
from importlib.machinery import SourceFileLoader
import config as cfgdeploy

def check_deployment_status(urldeployment,debug):
    #--------------------------------------------------------------------------
    # Function: check_deployment_status
    # Description: Attempt to check a deployment status for given deployment URL
    # Parms:
    # string urldeployment - Ths is the current deployment URL to check
    # boolean debug - Output debug info 
    # Returns:
    # String - Returns current deployment status value
    #--------------------------------------------------------------------------
    try:

        # Get string buffer for HTTP response
        response = BytesIO()
        
        # Instantiate pycurl object
        c = pycurl.Curl()

        # Set verbose mode for troubleshooting
        if (cfgdeploy.enableverbose):
           c.setopt(pycurl.VERBOSE,cfgdeploy.verbositylevel)

        # Set the Appian site deployment status API url
        c.setopt(c.URL, urldeployment)

        # Set the required HTTP headers for Deployment REST API
        c.setopt(c.HTTPHEADER, [f"Appian-API-Key: {cfgdeploy.apikey}","Action-Type: export"])

        # Set get info
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
        
        # Print formatted JSON string if debugging
        if debug:
           print(json_formatted_str)

        return str(jsonobj['status'])
    
    except Exception as ex: # Catch and handle exceptions
        # Print exception info if debug
        if debug: 
           print(str(ex)) # set exit message for stdout
           print('Traceback Info') # output traceback info for stdout
           traceback.print_exc()       
        # Return ERROR flag    
        return "ERROR"
    
def check_deployment_status_json(urldeployment,debug):
    #--------------------------------------------------------------------------
    # Function: check_deployment_status_json
    # Description: Attempt to check a deployment status for given deployment URL
    # and return the resulting JSON
    # Parms:
    # string urldeployment - Ths is the current deployment URL to check
    # boolean debug - Output debug info 
    # Returns:
    # String - Returns current deployment status JSON
    #--------------------------------------------------------------------------
    try:

        # Get string buffer for HTTP response
        response = BytesIO()
        
        # Instantiate pycurl object
        c = pycurl.Curl()

        # Set verbose mode for troubleshooting
        if (cfgdeploy.enableverbose):
           c.setopt(pycurl.VERBOSE,cfgdeploy.verbositylevel)

        # Set the Appian site deployment status API url
        c.setopt(c.URL, urldeployment)

        # Set the required HTTP headers for Deployment REST API
        c.setopt(c.HTTPHEADER, [f"Appian-API-Key: {cfgdeploy.apikey}","Action-Type: export"])

        # Set get info
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
        
        # Print formatted JSON string if debugging
        if debug:
           print(json_formatted_str)

        return jsonobj
    
    except Exception as ex: # Catch and handle exceptions
        # Print exception info if debug
        if debug: 
           print(str(ex)) # set exit message for stdout
           print('Traceback Info') # output traceback info for stdout
           traceback.print_exc()       
        # Return no object
        return None
    
def download_deployment_results(url,outputfile,replace,debug):
    #--------------------------------------------------------------------------
    # Function: download_deployment_results
    # Description: Attempt to download results from selected URL
    # Parms:
    # string url - This is the current URL to check
    # string outputfile - This is the output file
    # Boolean replace - Replace output file. True=Replace, False=Do not replace
    # Boolean debug - Output debug info
    # Returns:
    # Boolean - True-Download complete, False-Error on download
    #--------------------------------------------------------------------------
    try:

        # Check for output file 
        if (os.path.exists(outputfile)):
            # Kill file if replace. Otherwise throw exists error 
            if (replace): 
                os.remove(outputfile)   
            else:
                raise Exception(f"File {outputfile} exists and --replace=True was not selected. Process cancelled.")     

        # Get tring buffer for HTTP response
        response = BytesIO()

        # Output status message
        print(f"Downloading package URL: {url}")
        print(f"To file: {outputfile}")

        # Instantiate pycurl object
        c = pycurl.Curl()

        # Set verbose mode for troubleshooting
        if (cfgdeploy.enableverbose):
           c.setopt(pycurl.VERBOSE,cfgdeploy.verbositylevel)

        # Set the Appian site deployment API url
        c.setopt(c.URL,url)

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
        print(f"HTTP response status code: {httpcode}")
        print(f"Writing results to output file: {outputfile}")

        # Output zip package to file
        ofile=open(outputfile,'wb')
        ofile.write(response.getvalue())
        ofile.close()
        
        # Get file size
        file_stats = os.stat(outputfile)    
        print(f"{file_stats.st_size} bytes were written")

        # Close response buffer
        response.close()
        
        return True
    
    except Exception as ex: # Catch and handle exceptions
        # Print exception info if debug
        if debug: 
           print(str(ex)) # set exit message for stdout
           print('Traceback Info') # output traceback info for stdout
           traceback.print_exc()       
        # Return False on error
        return False
   
    
def str2bool(strval):
    #-------------------------------------------------------
    # Function: str2bool
    # Desc: Constructor
    # :strval: String value for true or false
    # :return: Return True if string value is" yes, true, t or 1
    #-------------------------------------------------------
    return strval.lower() in ("yes", "true", "t", "1")

def trim(strval):
    #-------------------------------------------------------
    # Function: trim
    # Desc: Alternate name for strip
    # :strval: String value to trim. 
    # :return: Trimmed value
    #-------------------------------------------------------
    return strval.strip()

def rtrim(strval):
    #-------------------------------------------------------
    # Function: rtrim
    # Desc: Alternate name for rstrip
    # :strval: String value to trim. 
    # :return: Trimmed value
    #-------------------------------------------------------
    return strval.rstrip()

def ltrim(strval):
    #-------------------------------------------------------
    # Function: ltrim
    # Desc: Alternate name for lstrip
    # :strval: String value to ltrim. 
    # :return: Trimmed value
    #-------------------------------------------------------
    return strval.lstrip()
    