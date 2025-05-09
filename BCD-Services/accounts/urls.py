from django.urls import path
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

    path('memo-image/', ImageUploadView.as_view(), name='upload-image'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)