from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password

from .serializers import PersonalDetailsSerializer, ImageUploadSerializer
from .models import ImageUpload

# Importing from firebase_config.py
from firebase_config import db
# For generating unique user ID
import uuid

@api_view(['GET', 'POST'])
def personal_details_view(request):
    if request.method == "GET":
        
        # Getting all data from 'personal_details' 
        people = db.child("personal_details").get().val()
        reordered_people = []
        
        # Making the User ID to be the first key in display
        if people:
            for person in people.values():
                reordered = {'User_id': person.get('User_id')}
                reordered.update({k: v for k, v in person.items() if k != 'User_id'})
                reordered_people.append(reordered)
                
        # It's return the user
        return Response(reordered_people)

    elif request.method == "POST":
        
        # Validating the data given by the user
        serializer = PersonalDetailsSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Generating the unique user ID
            user_id = data.get("User_id") or str(uuid.uuid4())
            data['User_id'] = user_id

            # Hashing the password before storing
            data['Password'] = make_password(data.pop('password'))

            # Storing the data under 'personal_details' in Firebase
            db.child("personal_details").child(user_id).set(data)

            return Response({
                "message": "Personal Details added successfully!",
                "data": data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
def personal_detail_view(request, user_id):
    
    # Fetching the user data & store it in 'person'
    ref = db.child("personal_details").child(user_id)
    person = ref.get().val()

    # Error , if user is not found
    if not person:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(person)

    # Update the user details
    elif request.method == "PUT":
        serializer = PersonalDetailsSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if 'password' in data:
                data['Password'] = make_password(data.pop('password'))
            ref.update(data)
            return Response({
                "message": "Personal details updated successfully",
                "data": data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Remove the user
    elif request.method == "DELETE":
        ref.remove()
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

            return JsonResponse({"message": "Cancer data submitted successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
