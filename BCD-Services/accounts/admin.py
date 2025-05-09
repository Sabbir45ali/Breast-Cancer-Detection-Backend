from django.contrib import admin
from .models import PersonalDetails, ImageUpload


@admin.register(PersonalDetails)
class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = ('User_id', 'First_Name', 'Last_Name', 'Mail_id', 'Phone_no')
    search_fields = ('User_id', 'First_Name', 'Last_Name', 'Mail_id')
    list_filter = ('First_Name', 'Last_Name')
    readonly_fields = ('Password',)
    fieldsets = (
        ('User Information', {
            'fields': ('User_id', 'First_Name', 'Middle_Name', 'Last_Name')
        }),
        ('Contact & Login', {
            'fields': ('Phone_no', 'Mail_id', 'Password', 'Profile_Pic')
        }),
    )


@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    search_fields = ('name',)
