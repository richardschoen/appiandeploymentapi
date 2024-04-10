# Sample Appian Application for access to Deployment REST API
The steps below describe how to set up the Appian ```Deployment REST API Sample Application``` so the REST API can be accessed from the Appian environment

## Create new application
Create a new application in Appian titled: ```Deployment REST API Sample Application```

Use ```DA``` as the prefix or whatever you desire.

## Create Connected System Named: DA Appian Deployment API
Create a new connected system to access the Deployment REST API from within Appian named: ```DA Appian Deployment API```   

Description: ```Appian Deployment API Connected System```   

Base URL: ```https://your instance.appiancloud.com```   

Authentication: ```API Key```   

Header Name: ```Appian-API-Key```   

Value: ```Paste Your API Key```   

Click ```Save``` to save the connected system.

Created connected system user interface example:   
![image](https://github.com/richardschoen/appiandeploymentapi/assets/9791508/d63333f6-1b08-4ee3-9044-e688061de9d7)

## Create New Integration Named: DA_GetDeploymentPackages
Create a new system integration system to access the Deployment REST API  via connected systemn within Appian named: ```DA_DeploymentPackages```   

### Rule Inputs
appid - This is a single text value to receive the application UUID you want to list packages for. 

### Integration Settings   
Connection: ```Use a Connected System```

Connected System: ```DA Appian Deployment API```   
Set to: ```Inherit Base URL```

Base URL: ```Should get set to the Base URL from the Connected System```

Relative Path: ```concat("/suite/deployment-management/v2/applications/",ri!appid,"/packages")```

Method: ```Get```

Timeout (sec): ```10```

Usage: ```Queries data```

Headers - Name: ```Action-Type```  Value: ```export```   

Ignore HTTP headers with empty values: `Checked/Enabled```

Response Body Parsing: ```Convert JSON to Appian value```   

Click ```Test Request``` to test the integration with an appid or ```Save Changes``` to save the integration.

Integration config screen shots:
![image](https://github.com/richardschoen/appiandeploymentapi/assets/9791508/22fb34df-2038-49a9-9f12-83127f079d7f)

![image](https://github.com/richardschoen/appiandeploymentapi/assets/9791508/6c0ee6b0-794e-438b-8e3e-d3039cae6ea8)

## Create DA_GetDeployementPackages Expression Rule
Create a new user expression rule and name it: ```DA_GetDeploymentPackages```

Create a single text parameter named: ```appid``` to receive the application inuqie ID (UUID)

Paste the SAIL from file: ```DA_GetDeploymentPackages_Expr.sail```

Click ```Save Changes```

Create expression rule screen shot:   
![image](https://github.com/richardschoen/appiandeploymentapi/assets/9791508/c97eb0af-d609-4e2d-a5c3-897127423d67)


## Create DA_PackageInformation User Interface
This user interface can be used to locate and list all packages and the UUID package ids for each package within an application.    

The user will enter an application UUID which can be determined from the Appian Application Properties.   

Create a new user interface and name it: ```DA_PackageInformation```

Switch to expression mode and paste the User Interface SAIL from file: ```DA_PackageInformation_UI.sail```

Click ```Save Changes```

Sample DA_PackageInformation User Interface:
<img width="1205" alt="image" src="https://github.com/richardschoen/appiandeploymentapi/assets/9791508/46d5eafc-b4ff-4fa0-8ba6-0d0636a98227">

