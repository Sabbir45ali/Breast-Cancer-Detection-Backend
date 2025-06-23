from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Imported views for URL Routing
from .views import (
    ImageUploadView,
    personal_details_view,
    personal_detail_view,
    submit_cancer_data
)

urlpatterns = [
    path('memo-image/', ImageUploadView.as_view(), name='upload-image'),
    path('cancer-data/', submit_cancer_data, name='submit-cancer-data'),
    path('personal-details/', personal_details_view, name='personal-details'),
    path('personal-details/<str:user_id>/', personal_detail_view, name='personal-detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
