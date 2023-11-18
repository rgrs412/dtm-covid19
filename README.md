## Demo Video
https://drive.google.com/file/d/1kDZpD0_wPBJ18Lqhb9_FBKbwyhqntL68/view?usp=drive_link

## Instructions to run app

(Optional) Create a python virtual environment
1) Enter the following command or your system's equivalent
to install all the necessary python packages:

pip install -r requirement.txt

2) Start the python or python3 terminal from your command prompt
and do the following:
from dtm_covid19 import db
db.create_all()
exit()

It should look like below:
<p>
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:06:47) [MSC v.1914 32 bit (Intel)] on win32 <br>
Type "help", "copyright", "credits" or "license" for more information.<br>
>>>from dtm_covid19 import db<br>
>>>db.create_all()<br>
>>>exit()
</p>

3) If you want to clear database and recreate it again, do the following:
db.drop_all()
db.create_all()

4) Enter the following or equivalent command into the command prompt to run the app:
python run.py

5) Go to http://localhost:8080/

6) Register for an account on the 'Sign Up Now' link with a fake email.
The email will work as long as it's in email format.

7) Sign in with the email and password you entered during registration.
