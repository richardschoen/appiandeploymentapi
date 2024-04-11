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

Usage:
```
python3 appian_packagelist.py --appid=yourappianapplicationuuid
```
