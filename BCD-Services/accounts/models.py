from django.db import models
from django.core.validators import RegexValidator


class PersonalDetails(models.Model):
    User_id = models.CharField(
        max_length=255,
        primary_key=True,
        unique=True
    )
    First_Name = models.CharField(max_length=255)
    Middle_Name = models.CharField(max_length=255, blank=True, null=True)
    Last_Name = models.CharField(max_length=255)
    Phone_no = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid phone number.")]
    )
    Mail_id = models.EmailField(unique=True)
    Password = models.CharField(max_length=255)  # Hashed in serializer
    Profile_Pic = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.First_Name} {self.Last_Name} ({self.User_id})"


class ImageUpload(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return f"Image: {self.name}"