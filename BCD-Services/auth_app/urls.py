from django.urls import path
from .views import signup_user, login_user,signup_org,login_org,login_admin




urlpatterns = [
    path('signup/', signup_user, name='signup'),
    path('login/', login_user, name='login'),
    path("signup-org/", signup_org, name="signup_org"),
    path("login-org/", login_org, name="login_org"), 
    path("login-admin/", login_admin, name="login_admin"), 
]
