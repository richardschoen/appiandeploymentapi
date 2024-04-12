##-------------------------------------------------------------------------------
## PowerShell Script Name: pwsh_listpackages.ps1
## Desc: List Appian Packages
##
## Parameters:
## $appid - Application uuid from Appian Application Properties
## 
## Links:
## https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-7.4
## https://4bes.nl/2020/08/23/calling-a-rest-api-from-powershell/
## Parse content
## https://stackoverflow.com/questions/64871235/iterating-through-invoke-webrequest-json-result
## https://education.launchcode.org/azure/chapters/powershell-intro/cmdlet-invoke-restmethod.html
## https://stackoverflow.com/questions/38622526/invoke-restmethod-how-do-i-get-the-return-code
## Format Strings
## https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-string-substitutions?view=powershell-7.4
##
## Returns:
## ExitCode or 0=success, 99=errors
##-------------------------------------------------------------------------------

## Defined parameters
param(
[string]$appid="",
[string]$ExitType="EXIT"
)

## Load shared PowerShell Macro functions or config settings
## Should be in same directory as this script
$ScriptDir = Split-Path $MyInvocation.MyCommand.Path 
Import-Module (Join-Path $ScriptDir "config.ps1")
#Import-Module ./config.ps1

## Init initial work variables
$exitcode=0
$lasterror=""

##-------------------------------------------------------------------------------
## Sample custom PowerShell function to write output to command line.
## Illustrates creating a custom PowerShell function.
##-------------------------------------------------------------------------------
function outputtext
{
Param ([string] $strValue)
Write-Output $strValue
}

##-------------------------------------------------------------------------------
## Let's try to do our work now and nicely handle errors
## This script should always end normally with an appropriate exit code
##-------------------------------------------------------------------------------
try {

        # Check if appid is empty. Bail if no app ID passed
        if ($appid.Trim() -eq "") {
          throw [System.Exception]::new("-appid parameter is required.") 
        }

        # Set Appian API Key HTTP Header
        $headers = @{
        'Appian-API-Key' = $apikey
        }
        
        # Build full URL for web service call
        $tempurl="$($siteurl)/suite/deployment-management/v2/applications/$($appid)/packages"

        $response=Invoke-WebRequest -Uri $tempurl -Headers $headers -Method Get
        
        Write-Output "Raw JSON Response:"
        Write-Output $response.Content # JSON response
        Write-Output $("HTTP response: "+ $response.StatusCode) # HTTP respone status code
        Write-Output ""

        # COnvert from JSON to Object
        $jsondata = $response.Content | ConvertFrom-Json

        # Output the response Object field by field. Alternative 1
        Write-Output "Package response object:"
        $jsondata.packages 

        # Output packages as a table. Alternative 2
        Write-Output "Package response as formatted table:"
        $jsondata.packages | Format-Table name,description,uuid,objectCount 

        ## Set completion info
        $exitcode=0
        $lasterror="Package list for app:$appid completed successfully."

        ## Write completion info
        Write-Output "ExitCode: $exitcode"
        Write-Output ("Message: " + $lasterror)
        #Write-Output "StackTrace: $_.Exception.StackTrace" 

        exit $exitcode

      }
##-------------------------------------------------------------------------------
## Catch and handle any errors and return useful info via console
##-------------------------------------------------------------------------------
catch [System.Exception] {
	$exitcode=99
  
  ## Error occurred
	Write-Output "ExitCode: $exitcode"
	Write-Output ("Message: " + $_.Exception.Message + " Line:" + $_.InvocationInfo.ScriptLineNumber.ToString() + " Char:" + $_.InvocationInfo.OffsetInLine.ToString())
  Write-Output "StackTrace: $_.Exception.StackTrace" 

  exit $exitcode

} finally {
}
