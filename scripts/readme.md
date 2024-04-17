# Appian Deployment REST API Scripts
This folder contains the sample Appian Deployment REST API scripts.

## config.py - Configuration settings file
This file holds general Python appp settings for the deployment app.

## config.sh - Configuration settings file
This file holds general Bash app settings for the deployment app.

## deployfunctions.py - General deployment functions used by scripts
This module contains general deployment functions used by the deployment scripts.

## appian_exportapplication.py - Export selected application
This script will take an application uuid as input parameter and will export the application to a ZIP package along with log output.

## appian_exportpackage.py - Export selected package
This script will take an application package uuid as input parameter and will export the package to a ZIP package along with log output.

## appian_packagedetails.py - List Packages for Application
This script will take an application uuid as input parameter and will list all the associated packages. 

Parms:
```--appid``` - Appian Application UUID

Usage example:
```
python3 appian_packagelist.py --appid=yourappianapplicationuuid
```
## appian_selectpackagedetails.py - List Packages for Application and Select One Based on package uuid, name or desc
This script will take an application uuid as input parameter. It will also accept a selecttype value for determining if you want to select a package based on packageuuid, packagename or packagedesc. It will list all the associated packages and also the one that is selected. This is meant to be a sample to show how to select a package by something other than just the package UUID. Your package name and desc can be crafted to match your DevOps tickets and stories and be selected accordingly for package export.    

Parms:
```--appid``` - Appian Application UUID
```--selecttype``` - Select type choices are ```packageuuid```, ```packagename``` or ```packagedesc```.   

Usage example to select package by name:
```
python3 appian_selectpackagelist.py --appid=yourappianapplicationuuid --selecttype=packagename --selectvalue="My Package 1"
```
