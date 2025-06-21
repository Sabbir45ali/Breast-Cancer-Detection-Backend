from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageUploadView, personal_detail_view, submit_cancer_data
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    personal_details_view,
    personal_detail_view,
    ImageUploadView
)

urlpatterns = [

    path('personal-details/', personal_details_view, name='personal-details'),
    path('personal-details/<str:user_id>/', personal_detail_view, name='personal-detail'),
    path('cancer-data/', submit_cancer_data, name='submit-cancer-data'),
    path('memo-image/', ImageUploadView.as_view(), name='upload-image'),
]; 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

