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
Also make sure that you have the correct driver installed. You will need "ODBC Driver for SQL Server"


Next add these values to the to the local.settings.json file

make sure to fill in the appropriate values
```bash
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
```
Next to test it out go to the run and debug menu and click run.
<img width="1068" height="505" alt="image" src="https://github.com/user-attachments/assets/f19d72b8-2f3a-459c-85cd-7741eab53c2f" />

If you see this the database is communicating correctly

Lets test to see if messages go through now.

Go to your azure portal and go to your Storage Account and go to queue

Click your database and click + Add message

Add a basic message
<img width="1542" height="827" alt="image" src="https://github.com/user-attachments/assets/d4e1d80e-cfd2-4c9c-bc9c-2b66b321dfbd" />

You should see your terminal look like this

<img width="1483" height="560" alt="image" src="https://github.com/user-attachments/assets/9280c3a8-89de-42b2-ad95-77ae0fd9dd1e" />

where Functions.OrderProcessor is working great and taking in the new orders!

We have successfully made a working and functioning database now


Now lets get this onto Azure

Make an Azure Function App
<img width="1572" height="2100" alt="Screenshot 2025-07-29 114000" src="https://github.com/user-attachments/assets/044fe5bb-4d2f-42b9-b928-85e606ce7b9f" />

Once deployed go back to VSCode and open up the azure sidebar extension. There are other ways to do this but this is the eaisest to do

Go to your resource and right click it and push deloy to function app...
<img width="2012" height="1510" alt="image" src="https://github.com/user-attachments/assets/68d6850d-04a0-4f81-bc09-1540b5c482d6" />

You should see this
<img width="2012" height="1510" alt="image" src="https://github.com/user-attachments/assets/62e2bc53-6658-497d-8ae1-7020f463c5d1" />

Next since we were just testing we are still using our Admin creds. Lets make sure that we don't have them exposed. 

Lets set up Role Based Access Control (RBAC)

<img width="1572" height="1237" alt="image" src="https://github.com/user-attachments/assets/2d25f9a0-d069-4610-81d7-c573e3a4fdbf" />

Now lets give access to the function to make changes to the database using this query

<img width="2050" height="1237" alt="image" src="https://github.com/user-attachments/assets/d94b5c12-abc5-4120-a6af-7c01dceb4c7b" />

Now that it is deployed putting in manual queues into the storage account that you made, it will get proccessed and put into the database all through azure!
