from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Replace with your actual models and serializers
# from .models import PersonalDetails
# from .serializers import PersonalDetailsSerializer, ImageUploadSerializer

@api_view(['GET', 'POST'])
def personal_details_view(request):
    if request.method == "GET":
        people = PersonalDetails.objects.all()
        serializer = PersonalDetailsSerializer(people, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = PersonalDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Personal details created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def personal_detail_view(request, user_id):
    try:
        person = PersonalDetails.objects.get(User_id=user_id)
    except ObjectDoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PersonalDetailsSerializer(person)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = PersonalDetailsSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Personal details updated successfully",
                "data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        person.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            print(">>> File stored at:", instance.image.url)
            return Response({
                "message": "Image uploaded successfully",
                "url": instance.image.url,
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def submit_cancer_data(request):
    if request.method == "POST":
        try:
            # Add your data handling logic here
            return JsonResponse({"message": "Cancer data submitted successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
