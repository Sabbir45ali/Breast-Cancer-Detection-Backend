import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .serializers import SignupSerializer, LoginSerializer
import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)  # parent directory of auth_app
from firebase_config import db




@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        serializer = SignupSerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse({"error": serializer.errors}, status=400)

        username = serializer.validated_data["username"]
        phnumber = serializer.validated_data["phnumber"]
        email = serializer.validated_data["email"]
        raw_password = serializer.validated_data["password"]

        # Check for existing username/email/phone
        all_users = db.child("user_login_details").get().val() or {}
        for user in all_users.values():
            if user.get("username") == username:
                return JsonResponse({"error": "Username already exists"}, status=400)
            if user.get("email") == email:
                return JsonResponse({"error": "Email already exists"}, status=400)
            if user.get("phnumber") == phnumber:
                return JsonResponse({"error": "Phone number already exists"}, status=400)

        # Save new user with hashed password
        hashed_password = make_password(raw_password)
        new_user = {
            "username": username,
            "phnumber": phnumber,
            "email": email,
            "password": hashed_password,
        }
        db.child("user_login_details").push(new_user)

        return JsonResponse({"message": "Signup successful"}, status=201)

    return JsonResponse({"error": "Only POST allowed"}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        serializer = LoginSerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse({"error": serializer.errors}, status=400)

        username = serializer.validated_data["username"]
        raw_password = serializer.validated_data["password"]

        # Fetch all users
        all_users = db.child("user_login_details").get().val() or {}
        for user in all_users.values():
            if user.get("username") == username:
                hashed_password = user.get("password")
                if check_password(raw_password, hashed_password):
                    return JsonResponse({"message": "Login successful"}, status=200)
                return JsonResponse({"error": "Invalid password"}, status=401)

        return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({"error": "Only POST allowed"}, status=405)
