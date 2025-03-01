
# Django Project Setup Guide

## Prerequisites
Ensure you have the following installed before proceeding:

1. **Python (>= 3.x)** - Download from [python.org](https://www.python.org/)
2. **pip** (Python package manager) - Comes with Python installation
3. **Virtualenv** - Install using `pip install virtualenv`
4. **Git** - Download from [git-scm.com](https://git-scm.com/)

---

## Installation and Setup

### Step 1: Go into the Project Directory
```bash
cd BCD-Services
```

### Step 2: Create a Virtual Environment
```bash
python -m venv myenv
```

### Step 3: Activate the Virtual Environment
**Windows:**
```bash
myenv\Scripts\activate
```
**macOS/Linux:**
```bash
source myenv/bin/activate
```

### Step 4: Install Required Dependencies
```bash
pip install -r requirements.txt
```
If an error occurs, try:
```bash
python -m pip install -r requirements.txt
```

### Step 5: Install Django if Not Installed
If you see 'Could Not Import Django', run:
```bash
pip install django
```

### Step 6: Register the App in `settings.py` (if not registered)
Edit `backend_site/settings.py` and add the app to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    'accounts.apps.AppNameConfig',
]
```

### Step 7: Apply Migrations and Create a Superuser
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Step 8: Install Pillow (If You Encounter ImageField Errors)
```bash
pip install pillow
```

### Step 9: Ensure the Migration Folder Exists
If your migration folder is missing, run:
```bash
python manage.py makemigrations accounts
python manage.py migrate accounts
```

### Step 10: Run the Development Server
```bash
python manage.py runserver
```
Access the application at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Troubleshooting
- If migrations fail, try deleting the `migrations/` folder inside the app and rerun migrations.
- If dependencies are missing, manually install them using `pip install <package-name>`.
- Ensure your virtual environment is activated before running any Django commands.

---


