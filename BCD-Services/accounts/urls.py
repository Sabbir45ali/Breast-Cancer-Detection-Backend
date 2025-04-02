from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonalDetailsViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'personal-details', PersonalDetailsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)