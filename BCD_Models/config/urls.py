from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.accounts.urls')),
    path('api/', include('backend.prediction.urls')),
]