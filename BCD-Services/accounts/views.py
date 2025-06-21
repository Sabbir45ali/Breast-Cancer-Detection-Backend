from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from .models import PersonalDetails, ImageUpload
from .serializers import PersonalDetailsSerializer, ImageUploadSerializer
from .serializers import ImageUploadSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import CancerData

from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['GET', 'POST'])
def personal_details_view(request):
    if request.method == "GET":
        people = PersonalDetails.objects.all()
        serializer = PersonalDetailsSerializer(people, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = PersonalDetailsSerializer(data=request.data)  # Explicitly pass request.data
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Personal details created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
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
        serializer = PersonalDetailsSerializer(person, data=request.data)  # Explicitly pass request.data
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Personal details updated successfully", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        person.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # ✅ Required for file uploads

    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            print(">>> File stored at:", instance.image.url)  # Should now be Cloudinary URL
            return Response({
                "message": "Image uploaded successfully",
                "url": instance.image.url,
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def submit_cancer_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Extract values from JSON
            radius_mean = data.get("radius_mean")
            texture_mean = data.get("texture_mean")
            area_mean = data.get("area_mean")
            smoothness_mean = data.get("smoothness_mean")
            compactness_mean = data.get("compactness_mean")
            concavity_mean = data.get("concavity_mean")

            # Validation: Ensure all values are present
            if None in [radius_mean, texture_mean, area_mean, smoothness_mean, compactness_mean, concavity_mean]:
                return JsonResponse({"error": "All fields are required"}, status=400)

            # Save to database
            CancerData.objects.create(
                radius_mean=radius_mean,
                texture_mean=texture_mean,
                area_mean=area_mean,
                smoothness_mean=smoothness_mean,
                compactness_mean=compactness_mean,
                concavity_mean=concavity_mean
            )

            return JsonResponse({"message": "Data saved successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

