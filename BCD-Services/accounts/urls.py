from django.urls import path
from .views import ImageUploadView

urlpatterns = [
    path('memo-image/', ImageUploadView.as_view(), name='upload-image'),
]
