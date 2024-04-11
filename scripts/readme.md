# Appian Deployment REST API Scripts
This folder contains the sample Appian Deployment REST API scripts.

## deployfunctions.py - General deployment functions used by scripts
This module contains general deployment functions used by the deployment scripts.

## appian_packagedetails.py - List Packages for Application
This script will take an application uuid as input parameter and will list all the associated packages. 

Parms:
```--appid``` - Appian Application UUID

Usage:
```
python3 appian_packagelist.py --appid=yourappianapplicationuuid
```
