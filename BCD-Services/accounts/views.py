from rest_framework import viewsets
from .models import PersonalDetails
from .serializers import PersonalDetailsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import CancerData

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

@csrf_exempt

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