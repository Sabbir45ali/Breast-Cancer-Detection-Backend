# Importing the 'redirect' the user to a new url as ,
# Django -> localhost 8000
# React -> localhost 3000

from django.shortcuts import render , redirect
from django.http import JsonResponse

# Redirect the user to the React Frontend Email confirmation page
def email_confirmation(request, key):
    return redirect(f"http://localhost:3000/dj-rest-auth/registration/account-confirm-email/{key}")

#Redirects the user to the React frontend password reset confirmation URL
def reset_password_confirm(request, uid, token):
    return redirect(f"http://localhost:3000/reset/password/confirm/{uid}/{token}")