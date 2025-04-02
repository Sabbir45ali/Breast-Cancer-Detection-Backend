from rest_framework import viewsets
from .models import PersonalDetails
from .serializers import PersonalDetailsSerializer

class PersonalDetailsViewSet(viewsets.ModelViewSet):
    queryset = PersonalDetails.objects.all()
    serializer_class = PersonalDetailsSerializer