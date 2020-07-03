# Stay Safe


## Team Members:

* Thomas Dolan
* Thomas Cochran
* Srivardhan Sajja


## Install the app (Linux):

1. Make a directory for the app and clone it:

    ``$ cd ~/Desktop``

    ``$ mkdir stay_safe``

    ``$ cd stay_safe``

    ``$ git clone https://github.com/tjdolan121/3308_App.git``
    
    ``$ cd 3308_App``

2. Install virtualenv (skip if already installed):

    ``$ python3 -m pip install --user virtualenv``

3. Create and activate a virtual environment:

    ``$ python3 -m venv venv``
    
    ``$ . venv/bin/activate``

4. Install dependencies:

    ``(venv)$ pip install -r requirements.txt``

5. Download the .env file attached attached to moodle for this assignment and put it in the 3308\_App directory

6. Create a sqlite3 database for the project:

    ``(venv)$ python manage.py makemigrations``

    ``(venv)$ python manage.py migrate``

7. Test that the app correctly runs by creating a local server (optional):
    
    ``(venv)$ python manage.py runserver``


## How to run tests:

1. Install the app in a virtual environment (see above). 

2. Re-locate static files to a single directory (mimics deployment; required for some tests cases):
    
    ``(venv)$ python manage.py collectstatic``

3. Run all test cases:

    ``(venv)$ python manage.py test``
    
4.  Run subset of test cases in apps/accounts/tests:
    
    ``(venv)$ python manage.py test apps.accounts.tests``   

5. Run subset of test cases in apps/pages/tests:

    ``(venv)$ python manage.py test apps.pages.tests``


## Test Cases:

#### Test 1:

- **Use case name:** 

    - Verify user login and authentication.


- **Description:** 

    - Test that a user can create an account and login to the application.


- **Pre-conditions:** 

    - User has navigated to the sign up page and correctly signed up by entering fields: 
        - username
        - password
        - email
        - first name
        - last name


- **Test Steps:** 

    - Navigate to the login page.
    - Provide the username and password given when signing up.
    - Click the login button.


- **Expected Result:** 

    - User should be able to login and view the home page.


- **Actual Result:** 

    - User's account is created and authenticated correctly.
    - The authenticated account can successfully navigate to the home page with HTTP status code 200.
    - The home page templates _base.html and home.html are rendered. 


- **Status (Pass/Fail):** 

    - Pass


- **Notes:** 

    - These tests use assertTemplateUsed(), which checks if a template is used when rendering a response.
    - assertTemplateUsed() requires django to collect static files for deployment.
    - View the test code for this case at: apps/pages/tests/test\_views.py
        
        - class TestUserLogin
        - class TestHomePageView
   
 
- **Post-conditions:** 

    - User's account object is created in the database and contains fields given during sign up.
    - User's account object has authentication status set to True.


#### Test 2:

- **Use case name:** 

    - Verify a user cannot add more than 5 emergency contacts.


- **Description:** 

    - Test that logged in users creating more than 5 emergency contacts are re-directed with an error.


- **Pre-conditions:** 

    - The user's account is created by signing up.
    - The user has logged in and navigated to the home page.


- **Test Steps:** 

    - Correctly enter an emergency contact by filling in the fields:
        - First name
        - Last name
        - Email (unique)
    - Press the Add Emergency Contact Button
    - Navigate back to the create emergency contact page by clicking the Set emergency contacts button.
    - Repeat this process five more times. 


- **Expected Result:** 

    - On the sixth attempt to create an emergency contact, the user is re-directed to the create emergency contact page with an error
    - The error should read: "Error: Maximum emergency contacts set."
    - The user should still have five emergency contacts in the database.


- **Actual Result:** 

    - The user is receieves a successful HTTP 200 status code when navigating to the create emergency contact page.
    - The add\_emergency\_contact.html and \_base.html templates are rendered correctly.
    - On the sixth attempt, an error message is generated with the handle 'max', with contents: "Error: Maximum emergency contacts set."
    - On the sixth attempt, the user is redirected to the create emergency contact page with a HTTP 302 redirect code. 
    - The user still has five emergency contacts in the database.


- **Status (Pass/Fail):** 

    - Pass


- **Notes:** 

    - These tests require django to collect static files for deployment in staticfiles/
    - View the test code for this case at: apps/pages/tests/test\_views.py
        
        - class TestEmergencyContactCreateView 


- **Post-conditions:** 

    - The user's account is associated with the first 5 emergency contacts entered.
    - The sixth emergency contact is not associated with the users account and does not exist in the database.


#### Test 3:

- **Use case name:** 

    - Verify that trips can be created and retain their assigned fields.


- **Description:** 

    - Test that a trip can be created and associated with a user account.
    - Test that the created trip has the following fields:
        - Name
        - Location
        - Start date
        - End date


- **Pre-conditions:** 

    - The user's account is created by signing up.
    - The user has logged in and navigated to the home page.


- **Test Steps:** 

    - Navigate to the create trip page by clicking the Create Trip button.
    - Correctly enter the fields:
        - Trip name/alias
        - Location
        - Start date: Set to tomorrow
        - End date: Set to three days from now
    - Click: Create Trip
    - At the home page, click: View Trips
    - Verify the trip you added exists on this page.


- **Expected Result:** 

    - The trip was successfully created.
    - The trip has the expected fields.


- **Actual Result:** 

    - A single trip object is created.
    - The expected fields exist and can be referenced as with the trip object.
    - The trip object is associated with the user that created the trip by the trip owner field.


- **Status (Pass/Fail):** 

    - Pass


- **Notes:** 

    - A database query for the user's account can also verify that this test passes (demo below).
        - After performing the above test steps, reference the user object from the database as follows:
            
            `(venv)$ python manage.py shell`
            
            `>>> from apps.accounts.models import CustomAccount`
            
            `>>> user = CustomAccount.objects.get(pk=1)`

            `>>> len(user.trips.all())`

            `>>> user.trips.all()[0].trip_name`

            `>>> user.trips.all()[0].trip_location`

    - The result should be: 
        - The user has one trip associated with their account.
        - The trip has the expected fields created during the test steps, e.g. trip_name, trip_location.

    - View the test code for this case at: apps/pages/tests/test\_views.py

        - TestTripModelFields


- **Post-conditions:** 

    - The user has one trip associated with their account with the expected fields.
    - The trip object and its attributes are logged in the database.
