# Sample Appian Application for access to Deployment REST API
The steps below describe how to set up the Appian ```Deployment REST API Sample Application``` so the REST API can be accessed from the Appian environment

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

Click ```Save``` to save the connected system.

Created connected system user interface example:   
![image](https://github.com/richardschoen/appiandeploymentapi/assets/9791508/d63333f6-1b08-4ee3-9044-e688061de9d7)


## Create DA_GetDeployementPackages Expression Rule
Create a new user expression rule and name it: ```DA_GetDeploymentPackages```

Create a single text parameter named: ```appid``` to receive the application inuqie ID (UUID)

Paste the SAIL from file: ```DA_GetDeploymentPackages_Expr.sail```

Click ```Save Changes```

## Create DA_PackageInformation User Interface
This user interface can be used to locate and list all packages and the UUID package ids for each package within an application.    

The user will enter an application UUID which can be determined from the Appian Application Properties.   

Create a new user interface and name it: ```DA_PackageInformation```

Switch to expression mode and paste the User Interface SAIL from file: ```DA_PackageInformation_UI.sail```

Click ```Save Changes```


