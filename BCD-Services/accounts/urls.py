from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageUploadView, PersonalDetailsViewSet, submit_cancer_data
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'personal-details', PersonalDetailsViewSet)
from .views import (
    personal_details_view,
    personal_detail_view,
    ImageUploadView
)
urlpatterns = [
    path('personal-details/', personal_details_view, name='personal-details'),
    path('personal-details/<str:user_id>/', personal_detail_view, name='personal-detail'),
    path('', include(router.urls)),
    path('memo-image/', ImageUploadView.as_view(), name='upload-image'),
]; 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)