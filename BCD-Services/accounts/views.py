from rest_framework import viewsets
from .models import PersonalDetails
from .serializers import PersonalDetailsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer

class PersonalDetailsViewSet(viewsets.ModelViewSet):
    queryset = PersonalDetails.objects.all()
    serializer_class = PersonalDetailsSerializer


class ImageUploadView(APIView):
    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Image uploaded successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
