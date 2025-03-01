from django.urls import path
from .views import (
    FormDataAll, FormDataView, FormDataCreate, FormDataUpdate, FormDataDelete,
    ImageUploadAll, ImageUploadView, ImageUploadCreate, ImageUploadDelete,
    api_status
)

urlpatterns = [

    path('form-data/all/', FormDataAll, name='form-data-all'),  
    path('form-data/view/<int:pk>/', FormDataView, name='form-data-view'),  
    path('form-data/create/', FormDataCreate, name='form-data-create'), 
    path('form-data/update/<int:pk>/', FormDataUpdate, name='form-data-update'), 
    path('form-data/delete/<int:pk>/', FormDataDelete, name='form-data-delete'), 


    path('image-upload/all/', ImageUploadAll, name='image-upload-all'),  
    path('image-upload/view/<int:pk>/', ImageUploadView, name='image-upload-view'), 
    path('image-upload/create/', ImageUploadCreate, name='image-upload-create'), 
    path('image-upload/delete/<int:pk>/', ImageUploadDelete, name='image-upload-delete'), 

    path('status/', api_status, name='api-status'),
]
