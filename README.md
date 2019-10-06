Quick and dirty script to send email reminders about assigned items in GDocs.


* Create a google app at https://console.developers.google.com
* Download your client ID and client Secret (oauth, json file) and save it as credentials.json in the same directory.
* In a pipenv or virtualenv, install the requirements and launch:

``` 
pip install -r requirements
python ./reminder.py
```

* Authorize your application. It should ask you to allow "View metadata for files in your Google Drive"
* Once authorized, a `token.json` file will be created. If you remove that file, you will have to re-authz the application.
