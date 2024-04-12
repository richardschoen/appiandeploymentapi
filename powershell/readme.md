# Appian Deployment REST API PowerShell Scripts
This folder contains the sample PowerShell Appian Deployment REST API scripts.   

The scripts are compatible with PowerShell 7.4.

## config.ps1 - Configuration settings file
This file holds general PowerShell app settings for the deployment app.

## pwsh_packagedetails.ps1 - List Packages for Application
This script will take an application uuid as input parameter and will list all the associated packages. 

Parms:
```-appid``` - Appian Application UUID

Usage:
```
pwsh pwsh_listpackages.ps1python3 -appid=yourappianapplicationuuid
```
