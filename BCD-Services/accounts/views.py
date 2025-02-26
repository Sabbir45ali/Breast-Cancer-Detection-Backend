from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import FormData, ImageUpload
from .serializer import FormDataSerializer, ImageUploadSerializer


@api_view(['GET'])
def FormDataAll(request):
    
    form_data = FormData.objects.all()
    serializer = FormDataSerializer(form_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def FormDataView(request, pk):
    
    form_data = get_object_or_404(FormData, pk=pk)
    serializer = FormDataSerializer(form_data)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def FormDataCreate(request):

    serializer = FormDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def FormDataUpdate(request, pk):

    form_data = get_object_or_404(FormData, pk=pk)
    serializer = FormDataSerializer(instance=form_data, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def FormDataDelete(request, pk):

    form_data = get_object_or_404(FormData, pk=pk)
    form_data.delete()
    return Response({'message': 'FormData deleted successfully!'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def ImageUploadAll(request):
    
    images = ImageUpload.objects.all()
    serializer = ImageUploadSerializer(images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def ImageUploadView(request, pk):

    image = get_object_or_404(ImageUpload, pk=pk)
    serializer = ImageUploadSerializer(image)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])  
def ImageUploadCreate(request):

    serializer = ImageUploadSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ImageUploadDelete(request, pk):

    image = get_object_or_404(ImageUpload, pk=pk)
    image.delete()
    return Response({'message': 'Image deleted successfully!'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def api_status(request):
    return Response({"message": "API is working!"}, status=status.HTTP_200_OK)