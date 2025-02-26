from django.db import models

class FormData(models.Model):
    
    user_id = models.CharField(max_length=100)
    radius = models.DecimalField(max_digits=10, decimal_places=4)
    texture = models.DecimalField(max_digits=10, decimal_places=4)
    smoothness = models.DecimalField(max_digits=10, decimal_places=4)
    area = models.DecimalField(max_digits=10, decimal_places=4)
    compactness = models.DecimalField(max_digits=10, decimal_places=4)
    concavity = models.DecimalField(max_digits=10, decimal_places=4)
    
    def __str__(self):
        
        return f"Data of {self.user_id}" 

class ImageUpload(models.Model):

    user_id = models.CharField(max_length=100)
    # it will automatically create a 'image' folder to store the images
    mammogram_image = models.ImageField(upload_to='image/')
    
    def __str__(self):
        
        return f"Image of {self.user_id}"