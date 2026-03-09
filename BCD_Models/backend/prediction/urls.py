from django.urls import path
from .views import (
    predict_image_api,
    org_predict_data,
    org_history,
    image_history,
    org_full_history,
    debug_ml_service
)
urlpatterns = [
    path('predict-image/', predict_image_api),
    path('org/predict-data/', org_predict_data),
    path('org/history/', org_history),
    path('image-history/', image_history),
    path('org/full-history/', org_full_history),
    path('debug-ml/', debug_ml_service),
]