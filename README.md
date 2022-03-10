# Team-4

> **Design**: An app which uses tkinter to simulate a whiteboard in python.
>
> **Requirements**: Python3, a virtual environment or python installation with the pip package manager and a Microsoft Office installation
>
> **Module-Installation**: You need a python installation and a pip packager for this to work. If you are running this on your local system you can use the following command: `pip install -r requirements.txt` If you are using replit git then once you delete requirements.txt replit should install all the necessary packages for you.
>
> **Setup**:  
> (1) Run start_app.py once your repo is setup. It will create whiteboards/security/unlock.key which must be linked.  
> (2) Copy the key generated in whiteboards/security/unlock.key to an environment variable named SECRET_KEY
> 
> *Your app should work now, if not it's probably for one of the following reasons...*  
> (1) **Replit**: If you pulled this repo on replit you must delete requirements.txt before running the start_app.py script, for some reason replit bugs out completely when given a requirements.txt file.  
> (2) **Bad Env Variable**: For the environment variable, it **must** be named exactly "SECRET_KEY" and contain a **value** equal to the contents of the file whiteboards/security/unlock.key. If this file does not exist you likely need to run start_app.py first to generate the file whiteboards/security/unlock.key.# Team-4

> `Design:` An app which uses tkinter to simulate a whiteboard in python.
>
> `Implementation:` Development
>
> `Requirements:` Python3, a virtual environment or python installation with the packages specified in requirements.txt and a Microsoft Office installation
>
> *Setup*: (1) Run start_app.py once your repo is setup. It will create whiteboards/security/unlock.key which must be linked.
>          (2) Link the key generated in whiteboards/security/unlock.key to an environment variable named SECRET_KEY
>          (3) Create a new xlsx document (excel) in whiteboards/userdata/ name it users (users.xlsx) and run encrypt_userfile.py