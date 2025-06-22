from django.contrib import admin
from .models import PersonalDetails, ImageUpload
from .models import PersonalDetails

@admin.register(PersonalDetails)
class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = ('User_id', 'First_Name', 'Last_Name', 'Mail_id', 'Phone_no') 
    search_fields = ('User_id', 'First_Name', 'Last_Name', 'Mail_id', 'Phone_no') 
    list_filter = ('First_Name', 'Last_Name') 