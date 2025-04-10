from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
import json

@csrf_exempt  # Only for testing! Use proper CSRF handling in production
def signup_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already taken"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already registered"}, status=400)

            # Create new user
            user = User.objects.create_user(username=username, email=email, password=password)
            token = Token.objects.create(user=user)

            return JsonResponse({
                "message": "Signup successful",
                "username": user.username,
                "token": token.key
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return JsonResponse({
                    "message": "Login successful",
                    "username": user.username,
                    "token": token.key
                }, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
