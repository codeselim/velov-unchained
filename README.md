velov-unchained
===============

## Vélo'v Renting System, without chains

### The webserver
To run the web application you must run first the webserver.  
From the folder **./web.py** run the following command:

    > python controller.py

By default the webserver will run on port 8080  
To run the webserver on a different port you can run the command as follows:

    > python controller.py 1234

The above command will run the webserver on the port 1234  
 
After running the webserver you can access the web application via `http://localhost:[port]`  

### The warning management system
To run the script updating the warning from the database  
From the folder **./web.py** run the following command:

	> python update_warnings.py


