from django.contrib import admin
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('accounts/', include('accounts.urls')),
    
    # Your app's custom URLs like signup
    path('auth/', include('auth_app.urls')),

    path('form/', include('accounts.urls')),  # Add this
    # 🔐 JWT Token endpoints (Login + Refresh)
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Token Refresh
]
