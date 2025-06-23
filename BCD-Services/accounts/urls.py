from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    ImageUploadView,
    personal_detail_view,
    personal_details_view,
    personal_detail_view,
    submit_cancer_data
)

router = DefaultRouter()
router.register(r'personal-details', personal_detail_view)

urlpatterns = [
    path('memo-image/', ImageUploadView.as_view(), name='upload-image'),
    path('cancer-data/', submit_cancer_data, name='submit-cancer-data'),
    path('', include(router.urls)),
    path('personal-details/', personal_details_view, name='personal-details'),
    path('personal-details/<str:user_id>/', personal_detail_view, name='personal-detail'),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
