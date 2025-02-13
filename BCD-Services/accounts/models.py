from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

# Custom user model extending AbstractBaseUser
# Replaces default Django user model with email-based authentication

class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    
    # Email filed as the primaray identifier
    email = models.EmailField(_("Email Address"), unique=True, max_length=255)

    # User details
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100, null=True, blank=True)

    # User status fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Timestamp fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # Use email as the username filed for authentication
    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = ['first_name']
    
    # Create a custom user manager
    objects = CustomUserManager()
    
    # String representation of the user
    def __str__(self):
        return self.email