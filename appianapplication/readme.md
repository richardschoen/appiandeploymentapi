# Sample Appian Application for access to deployment API
The steps below describe how to set up the Appian ```Deployment REST API Sample Application```.

## Create new application
Create a new application in Appian titled: ```Deployment REST API Sample Application```

Use ```DA``` as the prefix or whatever you desire.

## Create Connected System DA Appian Deployment API
Create a new connected system to access the Deployment REST API from within Appian named: ```DA Appian Deployment API```   

Description: ```Appian Deployment API Connected System```   

Base URL: ```https://your instance.appiancloud.com```   

Authentication: ```API Key```   

Header Name: ```Appian-API-Key```   

Value: ```Paste Your API Key```   

CLick ```Save``` to save the connected system.

## Create DA_GetDeployementPackages Expression Rule
Create a new user expression rule and name it: ```DA_GetDeploymentPackages```

Create a single text parameter named: ```appid``` to receive the application inuqie ID (UUID)

Paste the SAIL from file: ```DA_GetDeploymentPackages_Expr.sail```

Click ```Save Changes```

## Create DA_PackageInformation User Interface
Create a new user interface and name it: ```DA_PackageInformation```

Switch to expression mode and paste the User Interface SAIL from file: ```DA_PackageInformation_UI.sail```

Click ```Save Changes```


