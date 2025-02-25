Django Project Setup Guide

-> Prerequisites

Ensure you have the following installed before proceeding:

1: Python (>= 3.x)

2: pip (Python package manager)

3: Virtualenv

4: Git

-> Installation and Setup

Step 1: Create a Project Directory

mkdir project_name
cd project_name

Step 2: Create a Virtual Environment

python -m venv myenv

Step 3: Activate the Virtual Environment

Windows:

venv\Scripts\activate

macOS/Linux:

source venv/bin/activate

Step 4: Install Required Dependencies

pip install -r requirements.txt

Step 5: Create a Django Project

django-admin startproject project_name .

Step 6: Create a Django App

cd project_name
python manage.py startapp app_name

Step 7: Register the App in settings.py

Edit settings.py and add the app to INSTALLED_APPS:

INSTALLED_APPS = [
    'app_name.apps.AppNameConfig',
    'rest_framework',
    'corsheaders',
]

Step 8: Apply Migrations and Create a Superuser

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser


Step 9: Run the Development Server

python manage.py runserver

Access the application at http://127.0.0.1:8000/



