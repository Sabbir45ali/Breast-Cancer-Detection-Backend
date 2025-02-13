from django.contrib import admin
from django.urls import path , include

from accounts.views import email_confirmation , reset_password_confirm

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication endpoints from dj-rest-auth
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    
    # It's an Custom endpoint for email confirmation (always write it before dj-rest-registration)
    path('dj-rest-auth/registration/account-confirm-email/<str:key>', email_confirmation),
    
    # Resistration endpoints for dj-rest-auth
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # It's an Custom endpoint for email confirmation during password reset
    path('reset/password/confirm/<int:uid>/<str:token>' , reset_password_confirm , name = "password_reset_confirm"),
]
