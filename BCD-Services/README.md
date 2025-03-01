Django Project Setup Guide

-> Prerequisites

Ensure you have the following installed before proceeding:

1: Python (>= 3.x)

2: pip (Python package manager)

3: Virtualenv

4: Git

-> Installation and Setup

Step 1: Go into Project Directory

cd BCD-Services

Step 2: Create a Virtual Environment

python -m venv myenv

Step 3: Activate the Virtual Environment

Windows:

myenv\Scripts\activate

macOS/Linux:

source venv/bin/activate

Step 4: Install Required Dependencies

pip install -r requirements.txt

Step 5: Register the App in settings.py if not registered

Edit settings.py and add the app to INSTALLED_APPS:

INSTALLED_APPS = [
    'accounts.apps.AppNameConfig',
    'rest_framework',
    'corsheaders',
]

Step 8: Apply Migrations and Create a Superuser

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

Step 9: If Your Migration Folder Is Not Created Then Run , 

python manage.py makemigrations accounts
python manage.py migrate accounts

Step 10: Run the Development Server

python manage.py runserver

Access the application at http://127.0.0.1:8000/



