from django.urls import path
from .views import user_signup, org_signup, user_login, org_login, user_profile, org_profile, update_user_profile
urlpatterns = [
path('user/signup/', user_signup),
path('org/signup/', org_signup),
path('user/login/', user_login),
path('org/login/', org_login),
path('user/profile/', user_profile),
path('org/profile/', org_profile),
path('user/update-profile/', update_user_profile),
]