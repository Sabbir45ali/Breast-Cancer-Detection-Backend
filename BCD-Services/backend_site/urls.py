from django.contrib import admin
from django.urls import path , include

from accounts.views import email_confirmation , reset_password_confirm

urlpatterns = [
    path('admin/', admin.site.urls),
    
]
