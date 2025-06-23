from django.db import models
from django.core.validators import RegexValidator
from cloudinary_storage.storage import MediaCloudinaryStorage

class PersonalDetails(models.Model):
    User_id = models.CharField(max_length=255, primary_key=True, unique=True)
    First_Name = models.CharField(max_length=255)
    Middle_Name = models.CharField(max_length=255, blank=True, null=True)
    Last_Name = models.CharField(max_length=255)
    Phone_no = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid phone number.")]
    )
    Mail_id = models.EmailField(unique=True)
    Password = models.CharField(max_length=255)  # We'll hash this later
    Profile_Pic = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.First_Name} {self.Last_Name} ({self.User_id})"

class ImageUpload(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='uploads/')

    def __str__(self):
        return self.name

class CancerData(models.Model):
    radius_mean = models.FloatField()
    texture_mean = models.FloatField()
    area_mean = models.FloatField()
    smoothness_mean = models.FloatField()
    compactness_mean = models.FloatField()
    concavity_mean = models.FloatField()
    submitted_at = models.DateTimeField(auto_now_add=True)