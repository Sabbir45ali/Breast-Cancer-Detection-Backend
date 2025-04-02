from django.db import models
from django.core.validators import RegexValidator

class PersonalDetails(models.Model):
    User_id = models.CharField(max_length=255, primary_key=True, unique=True)
    First_Name = models.CharField(max_length=255)
    Middle_Name = models.CharField(max_length=255, blank=True, null=True)
    Last_Name = models.CharField(max_length=255)
    Phone_no = models.CharField(max_length=20, unique=True)
    Mail_id = models.EmailField(unique=True)
    Password = models.CharField(max_length=255)  # We'll hash this later
    Profile_Pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Use ImageField

    def __str__(self):
        return self.User_id