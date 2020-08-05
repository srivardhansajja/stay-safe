# Stay Safe Contributing Instructions

#### HOW  TO CONTRIBUTE (Instruction for Unix-type systems):

STEP 1: Clone the project (in the terminal): ```git clone git@github.com:tjdolan121/3308_App.git```

STEP 2: Create a new virtual environment: ```virtualenv venv```

STEP 3: Activate the virtual environment: ```source venv/bin/activate```

STEP 4: Navigate to the project directory (should contain "manage.py" file) and install requirements: ```pip install -r requirements.txt```

STEP 5: Obtain a SECRET_KEY: https://www.miniwebtool.com/django-secret-key-generator/

STEP 5: Create a .env file in the project directory

STEP 6: Add a secret key environment variable (in .env): ```SECRET_KEY=(paste key here)```

STEP 7: Run migrations (while in project directory): ```python manage.py migrate```

STEP 8: Create a superuser account: ```python manage.py createsuperuser```

STEP 9: Run server: ```python manage.py runserver```

STEP 10: Navigate to http://127.0.0.1:8000/admin in browser, log in with your super user account, and create some data.

### Feel free to message the team if you have any questions!