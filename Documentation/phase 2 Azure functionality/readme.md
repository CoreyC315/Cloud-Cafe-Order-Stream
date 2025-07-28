# First make sure that you are using python

Now create a function app using VScode

make sure that you have downloaded azure install on VScode.
<img width="778" height="641" alt="image" src="https://github.com/user-attachments/assets/d9d8d5e5-02b7-446e-8251-8c82e39693d5" />

press ctrl + shift + p and select "Azure Functions: Create New Project"

put it in the a subfolder
choose python and the version of python you are using
next choose Azure queue trigger
and link it to your storage account that you made in phase 1
Call it orderqueue

<img width="882" height="615" alt="image" src="https://github.com/user-attachments/assets/2bf43ead-97a9-494e-9059-229c4b48e931" />

After that you should be left with a function_app template.

Next activate your virtual enviroment that was made. So you don't interfere with your machines packages.
.\.venv\Scripts\activate

Next make sure you add pyodbc and azure-identity to the requirements.txt file to get the nessecary packages for communicating with the SQLdatabase

Next add these values to the to the local.settings.json file

make sure to fill in the appropriate values

{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "DefaultEndpointsProtocol=https;AccountName=YOUR_STORAGE_ACCOUNT_NAME;AccountKey=YOUR_FULL_STORAGE_ACCOUNT_ACCESS_KEY_GOES_HERE==;EndpointSuffix=core.windows.net",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "SQL_SERVER_NAME": "YOUR_SQL_SERVER_NAME.database.windows.net",
    "SQL_DATABASE_NAME": "SQL_DATABASE_NAME",
    "SQL_ADMIN_USER": "SQL_ADMIN_NAME",
    "SQL_ADMIN_PASSWORD": "YOUR_SQLADMIN_PASSWORD"
  },
  "Host": {
    "CORS": "*"
  }
}
